import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.convert_currency_service
import project.create_api_key_service
import project.oauth_token_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Currency Exchanger API",
    lifespan=lifespan,
    description="To accomplish the task of creating an endpoint that accepts a base currency, a target currency code, and a float value, and then retrieves real-time exchange rate data to calculate and return the converted value in the target currency, we will employ a tech stack comprising Python as the programming language, FastAPI as the API framework, PostgreSQL for the database, and Prisma as the ORM. The key steps and considerations for implementing this functionality are summarized below:\n\n1. **Python Package for Exchange Rates**: Use the 'forex-python' package, as it is a popular choice for fetching real-time exchange rate data. It allows for straightforward conversions and access to various financial information, including current currency exchange rates.\n\n2. **FastAPI Endpoint Implementation**: Create a FastAPI endpoint that can accept the mentioned parameters (base currency, target currency code, and a float value). This involves defining a route that accepts these parameters, either as query parameters or as part of a JSON payload, and returns a JSON response with the converted value. The route can be defined as follows:\n```python\nfrom fastapi import FastAPI\nfrom forex_python.converter import CurrencyRates\n\napp = FastAPI()\n\n@app.get('/convert')\ndef convert_currency(base: str, target: str, amount: float) -> dict:\n    c = CurrencyRates()\n    conversion_rate = c.get_rate(base, target)\n    converted_amount = conversion_rate * amount\n    return {'converted_amount': converted_amount}\n```\n\n3. **Prisma with PostgreSQL**: For this task, the primary focus is on fetching and converting currency values in real-time, which might not require direct interaction with PostgreSQL and Prisma unless there's a need to store transaction or conversion histories. If data persistence is desired, Prisma can be configured to interact with PostgreSQL for storing details of each conversion operation. This would involve defining a model for the conversion operations in the `schema.prisma` file and using Prisma Client for database operations in the FastAPI application.\n\n4. **Returning the Converted Value**: Ensure the endpoint correctly fetches the exchange rate between the base and target currencies using 'forex-python', performs the conversion with the provided float value, and then returns the result in the response. This process is encapsulated in the FastAPI route as shown in the code snippet above.\n\nBy integrating these components, we can develop a robust system for real-time currency conversion that leverages FastAPI's efficiency and 'forex-python's comprehensive currency exchange functionalities.",
)


@app.post(
    "/auth/api-key", response_model=project.create_api_key_service.CreateApiKeyResponse
)
async def api_post_create_api_key(
    userId: str, apiKeyPurpose: str
) -> project.create_api_key_service.CreateApiKeyResponse | Response:
    """
    Generates a new API key for authenticated users, allowing server-to-server communication.
    """
    try:
        res = await project.create_api_key_service.create_api_key(userId, apiKeyPurpose)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/token", response_model=project.oauth_token_service.OAuthTokenResponse)
async def api_post_oauth_token(
    client_id: str,
    client_secret: str,
    grant_type: str,
    code: Optional[str],
    refresh_token: Optional[str],
) -> project.oauth_token_service.OAuthTokenResponse | Response:
    """
    Exchanges OAuth 2.0 credentials for a token, enabling user authentication.
    """
    try:
        res = await project.oauth_token_service.oauth_token(
            client_id, client_secret, grant_type, code, refresh_token
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/convert/{base}/{target}/{amount}",
    response_model=project.convert_currency_service.ConvertCurrencyResponse,
)
async def api_get_convert_currency(
    base: str, target: str, amount: float
) -> project.convert_currency_service.ConvertCurrencyResponse | Response:
    """
    Converts a specified amount from a base currency to a target currency using real-time exchange rates.
    """
    try:
        res = project.convert_currency_service.convert_currency(base, target, amount)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )

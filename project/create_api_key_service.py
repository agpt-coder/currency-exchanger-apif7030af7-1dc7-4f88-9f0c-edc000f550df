import secrets
from datetime import datetime, timedelta

import prisma
import prisma.models
from pydantic import BaseModel


class CreateApiKeyResponse(BaseModel):
    """
    Contains the newly created API key, along with information regarding its usage and validity.
    """

    apiKey: str
    expiryDate: str
    purpose: str


async def create_api_key(userId: str, apiKeyPurpose: str) -> CreateApiKeyResponse:
    """
    Generates a new API key for authenticated users, allowing server-to-server communication.

    Args:
    userId (str): The unique identifier of the user requesting the API key.
    apiKeyPurpose (str): A brief description of the intended use for the API key, aiding in management and auditing.

    Returns:
    CreateApiKeyResponse: Contains the newly created API key, along with information regarding its usage and validity.
    """
    generated_api_key = secrets.token_urlsafe(32)
    expiry_date = datetime.now() + timedelta(days=365)
    api_key = await prisma.models.ApiKey.prisma().create(
        data={"key": generated_api_key, "User": {"connect": {"id": userId}}}
    )
    return CreateApiKeyResponse(
        apiKey=generated_api_key,
        expiryDate=expiry_date.strftime("%Y-%m-%d"),
        purpose=apiKeyPurpose,
    )

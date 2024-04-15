---
date: 2024-04-15T19:57:37.456948
author: AutoGPT <info@agpt.co>
---

# Currency Exchanger API

To accomplish the task of creating an endpoint that accepts a base currency, a target currency code, and a float value, and then retrieves real-time exchange rate data to calculate and return the converted value in the target currency, we will employ a tech stack comprising Python as the programming language, FastAPI as the API framework, PostgreSQL for the database, and Prisma as the ORM. The key steps and considerations for implementing this functionality are summarized below:

1. **Python Package for Exchange Rates**: Use the 'forex-python' package, as it is a popular choice for fetching real-time exchange rate data. It allows for straightforward conversions and access to various financial information, including current currency exchange rates.

2. **FastAPI Endpoint Implementation**: Create a FastAPI endpoint that can accept the mentioned parameters (base currency, target currency code, and a float value). This involves defining a route that accepts these parameters, either as query parameters or as part of a JSON payload, and returns a JSON response with the converted value. The route can be defined as follows:
```python
from fastapi import FastAPI
from forex_python.converter import CurrencyRates

app = FastAPI()

@app.get('/convert')
def convert_currency(base: str, target: str, amount: float) -> dict:
    c = CurrencyRates()
    conversion_rate = c.get_rate(base, target)
    converted_amount = conversion_rate * amount
    return {'converted_amount': converted_amount}
```

3. **Prisma with PostgreSQL**: For this task, the primary focus is on fetching and converting currency values in real-time, which might not require direct interaction with PostgreSQL and Prisma unless there's a need to store transaction or conversion histories. If data persistence is desired, Prisma can be configured to interact with PostgreSQL for storing details of each conversion operation. This would involve defining a model for the conversion operations in the `schema.prisma` file and using Prisma Client for database operations in the FastAPI application.

4. **Returning the Converted Value**: Ensure the endpoint correctly fetches the exchange rate between the base and target currencies using 'forex-python', performs the conversion with the provided float value, and then returns the result in the response. This process is encapsulated in the FastAPI route as shown in the code snippet above.

By integrating these components, we can develop a robust system for real-time currency conversion that leverages FastAPI's efficiency and 'forex-python's comprehensive currency exchange functionalities.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Currency Exchanger API'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow

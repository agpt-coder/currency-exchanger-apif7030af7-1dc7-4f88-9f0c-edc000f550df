from forex_python.converter import CurrencyRates
from pydantic import BaseModel


class ConvertCurrencyResponse(BaseModel):
    """
    Response model for currency conversion, providing the converted amount in the target currency.
    """

    converted_amount: float


def convert_currency(base: str, target: str, amount: float) -> ConvertCurrencyResponse:
    """
    Converts a specified amount from a base currency to a target currency using real-time exchange rates.

    Args:
        base (str): The ISO 4217 currency code for the base currency from which the conversion starts.
        target (str): The ISO 4217 currency code for the target currency to which the amount will be converted.
        amount (float): The amount in the base currency to be converted to the target currency.

    Returns:
        ConvertCurrencyResponse: Response model for currency conversion, providing the converted amount in the target currency.
    """
    currency_converter = CurrencyRates()
    conversion_rate = currency_converter.get_rate(base, target)
    converted_amount = float(conversion_rate) * amount
    return ConvertCurrencyResponse(converted_amount=converted_amount)

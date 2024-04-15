from typing import Optional

import httpx
from pydantic import BaseModel


class OAuthTokenResponse(BaseModel):
    """
    The response from the server containing the access and/or refresh tokens for the client.
    """

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


async def oauth_token(
    client_id: str,
    client_secret: str,
    grant_type: str,
    code: Optional[str] = None,
    refresh_token: Optional[str] = None,
) -> OAuthTokenResponse:
    """
    Exchanges OAuth 2.0 credentials for a token, enabling user authentication.

    Args:
        client_id (str): The client identifier as issued by the authorization server.
        client_secret (str): The client secret known only to the client and the authorization server.
        grant_type (str): Specifies the type of grant being requested by the client. Typically 'authorization_code' for the initial request, or 'refresh_token' for obtaining a new access token.
        code (Optional[str]): The authorization code received from the authorization server (not required for refresh_token grant type).
        refresh_token (Optional[str]): The refresh token received from the authorization server (required only for refresh_token grant type).

    Returns:
        OAuthTokenResponse: The response from the server containing the access and/or refresh tokens for the client.

    Example Usage:
        response = await oauth_token(client_id="your_client_id",
                                     client_secret="your_secret",
                                     grant_type="authorization_code",
                                     code="your_code")
    """
    token_endpoint = "https://your.authorizationserver.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": grant_type,
    }
    if grant_type == "authorization_code" and code:
        data["code"] = code
    elif grant_type == "refresh_token" and refresh_token:
        data["refresh_token"] = refresh_token
    else:
        raise ValueError(
            "Invalid grant_type or missing parameters (code or refresh_token) for the given grant_type."
        )
    async with httpx.AsyncClient() as client:
        response = await client.post(token_endpoint, data=data)
        response.raise_for_status()
        token_data = response.json()
        return OAuthTokenResponse(**token_data)

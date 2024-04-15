from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    The response returned by the system after attempting to authenticate a user. It includes an access token upon successful authentication or an error message.
    """

    access_token: str
    token_type: str
    expires_in: int
    error: Optional[str] = None


async def authenticate_user(username: str, password: str) -> LoginResponse:
    """
    Handles user authentication and returns an access token.

    Args:
    username (str): The username or email address of the user attempting to log in.
    password (str): The password associated with the user's account. This should be transmitted securely.

    Returns:
    LoginResponse: The response returned by the system after attempting to authenticate a user. It includes an access token upon successful authentication or an error message.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        token = "pseudo_jwt_token"
        response = LoginResponse(
            access_token=token, token_type="Bearer", expires_in=3600, error=None
        )
    else:
        response = LoginResponse(
            access_token="",
            token_type="Bearer",
            expires_in=0,
            error="Authentication failed. Username or password is incorrect.",
        )
    return response

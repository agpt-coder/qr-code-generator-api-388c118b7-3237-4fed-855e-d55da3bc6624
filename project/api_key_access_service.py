import prisma
import prisma.models
from pydantic import BaseModel


class ApiKeyAccessResponse(BaseModel):
    """
    This model defines the structured response returned after validating an API key. It includes a success message and potentially an indication of the access level granted.
    """

    message: str
    access_level: str


async def api_key_access(api_key: str) -> ApiKeyAccessResponse:
    """
    Validates an API key and returns successful access message.

    This function searches for a provided API key in the database and validates it. If the key is found and active,
    it returns a structured response with a success message and the level of access granted based on the user role associated
    with the API key. Otherwise, it raises an exception indicating the key is invalid or not found.

    Args:
        api_key (str): The API key provided by the user for validation.

    Returns:
        ApiKeyAccessResponse: This model defines the structured response returned after validating an API key. It includes
        a success message and potentially an indication of the access level granted.

    Example:
        key = "valid-api-key"
        response = await api_key_access(key)
        print(response)
        > message="API Key validated successfully", access_level="DEVELOPER"
    """
    api_key_record = await prisma.models.ApiKey.prisma().find_unique(
        where={"key": api_key}, include={"User": True}
    )
    if api_key_record is None:
        raise ValueError("API Key is not valid or does not exist.")
    access_level = api_key_record.User.role.name
    return ApiKeyAccessResponse(
        message="API Key validated successfully", access_level=access_level
    )

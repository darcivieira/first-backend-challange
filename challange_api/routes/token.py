from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from challange_api.helpers.auth import authenticate_user, refresh_token
from challange_api.serializers.token import TokenResponse, LoginTemplate, RefreshResponse

router = APIRouter(
    prefix="/token",
    tags=["Authentication"],
    responses={
        404: {'description': 'NotFound'}
    }
)


@router.post('/auth', response_model=TokenResponse, include_in_schema=False)
async def post(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    A method that allow you to authenticate by swagger documentation.

    Parameters:
        form_data: An instance of OAuth2PasswordRequestForm that represents the payload required to authenticate.

    Returns:
        A response body with both access and refresh token.
    """
    return authenticate_user(form_data.username, form_data.password)


@router.post('', response_model=TokenResponse)
async def post(form_data: LoginTemplate):
    """
    A method that allow you to authenticate by request.

    Parameters:
        form_data: An instance of LoginTemplate that represents the payload required to authenticate.

    Returns:
        A response body with both access and refresh token.
    """
    return authenticate_user(form_data.username, form_data.password)


@router.put('/refresh', response_model=TokenResponse)
async def put(token: RefreshResponse = Depends(refresh_token)):
    """
    A method that allow to update your tokens.

    Parameters:
        token: A response body with both access and refresh token.

    Returns:
        A response body with both access and refresh token.
    """
    return token

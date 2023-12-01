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
    return authenticate_user(form_data.username, form_data.password)


@router.post('', response_model=TokenResponse)
async def post(form_data: LoginTemplate):
    return authenticate_user(form_data.username, form_data.password)


@router.put('/refresh', response_model=TokenResponse)
async def put(token: RefreshResponse = Depends(refresh_token)):
    return token

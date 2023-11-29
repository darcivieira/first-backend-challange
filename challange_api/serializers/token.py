from pydantic import BaseModel, Field


class LoginTemplate(BaseModel):
    username: str = Field(None, description='Usuário utilizado para logar no sistema.')
    password: str = Field(None, description='Senha utilizada para logar no sistema.')


class RefreshResponse(BaseModel):
    refresh_token: str = Field(None, description='Token utilizado para renovação da sessão.')


class TokenResponse(RefreshResponse):
    access_token: str = Field(None, description='Token de sessão que deverá ser utilizado na sessão.')

from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30
    ROOT_PATH: str = '/api/v1'
    REDIS_HOST: str = 'redis'
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str


settings = Settings()


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token/auth")

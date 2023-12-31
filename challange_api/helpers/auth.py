from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from challange_api.models.users import Users
from challange_api.serializers.users import UserResponse
from challange_api.settings import settings, OAUTH2_SCHEME
from challange_api.utils.shortcuts import verify_password

session = Users.objects()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def generate_token(user):
    access_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"user": user.id}, expires_delta=access_expires)
    refresh_token = create_access_token(data={"user": user.id}, expires_delta=refresh_expires)
    return {'access_token': access_token, 'refresh_token': refresh_token}


def authenticate_user(username, password):
    user = session.get(email=username)
    if user and verify_password(password, user.password):
        return generate_token(user)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={"WWW-Authenticate": "Bearer"}
    )


def get_current_user(token: str = Depends(OAUTH2_SCHEME)) -> tuple[UserResponse, Session]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = session.get(user_id)
    if user is None:
        raise credentials_exception
    session.session.refresh(user)
    return user, session


def get_current_active_user(user_session: tuple[UserResponse, Session] = Depends(get_current_user)):
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return user_session


def refresh_token(user_session: tuple[UserResponse, Session] = Depends(get_current_user)):
    user, _ = user_session
    return generate_token(user)

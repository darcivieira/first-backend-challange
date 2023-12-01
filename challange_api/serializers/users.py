from enum import Enum
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, SecretStr, field_validator, Field
from challange_api.utils.dictionary import *


class UserType(str, Enum):
    common = 'common'
    shopkeeper = 'shopkeeper'


class UserModel(BaseModel):
    name: str = Field(description=USER_FIELD_NAME)
    register_number: str = Field(description=USER_FIELD_REGISTER_NUMBER)
    email: EmailStr = Field(description=USER_FIELD_EMAIL)
    type: UserType = Field(UserType.common, description=USER_FIELD_TYPE)


class UserResponse(UserModel):
    id: str = Field(description=FIELD_IDENTIFICATION)


class UserCreate(UserModel):
    password: SecretStr = Field(description=USER_FIELD_PASSWORD)

    @field_validator('register_number')
    @classmethod
    def validate_register_number(cls, value: str):
        try:
            int(value)
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"register_number": "Invalid data"}
            )
        else:
            if len(value) != 11 and len(value) != 14:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"register_number": "Invalid data"}
                )
        return value


class UserUpdate(UserCreate):
    name: Optional[str] = Field(None, description=USER_FIELD_NAME)
    register_number: Optional[str] = Field(None, description=USER_FIELD_REGISTER_NUMBER)
    email: Optional[EmailStr] = Field(None, description=USER_FIELD_EMAIL)
    type: Optional[UserType] = Field(None, description=USER_FIELD_TYPE)
    password: Optional[SecretStr] = Field(None, description=USER_FIELD_PASSWORD)

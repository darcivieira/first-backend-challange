from enum import Enum
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, SecretStr, field_validator, ValidationError


class UserType(str, Enum):
    common = 'common'
    shopkeeper = 'shopkeeper'


class UserModel(BaseModel):
    name: str
    register_number: str
    email: EmailStr
    type: UserType = UserType.common


class UserResponse(UserModel):
    id: str


class UserCreate(UserModel):
    password: SecretStr

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
    name: Optional[str] = None
    register_number: Optional[str] = None
    email: Optional[EmailStr] = None
    type: Optional[UserType] = None
    password: Optional[SecretStr] = None

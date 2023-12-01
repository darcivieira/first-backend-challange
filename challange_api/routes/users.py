from fastapi import APIRouter, Depends

from challange_api.controllers.users import UsersViewSet
from challange_api.generics.models import Manager
from challange_api.helpers.auth import get_current_active_user
from challange_api.serializers.users import UserResponse, UserCreate, UserUpdate
from challange_api.utils.dictionary import *

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={
        404: {'description': 'NotFound'}
    }
)


@router.get("", response_model=list[UserResponse], name=USER_LIST_NAME, description=USER_LIST_DESCRIPTION)
def list(user_manager: tuple[UserResponse, Manager] = Depends(get_current_active_user)):
    return UsersViewSet.list()


@router.post("", status_code=201, response_model=UserResponse, name=USER_CREATE_NAME, description=USER_CREATE_DESCRIPTION)
def create(body: UserCreate):
    return UsersViewSet.create(body)


@router.get("/{user_id}", response_model=UserResponse, name=USER_RETRIEVE_NAME, description=USER_RETRIEVE_DESCRIPTION)
def retrieve(user_id: str, user_manager: tuple[UserResponse, Manager] = Depends(get_current_active_user)):
    return UsersViewSet.retrieve(user_id)


@router.patch("/{user_id}", response_model=UserResponse, name=USER_UPDATE_NAME, description=USER_UPDATE_DESCRIPTION)
def patch(user_id: str, body: UserUpdate, user_manager: tuple[UserResponse, Manager] = Depends(get_current_active_user)):
    return UsersViewSet.update(user_id, body)


@router.delete("/{user_id}", status_code=204, response_model=None, name=USER_DELETE_NAME, description=USER_DELETE_DESCRIPTION)
def delete(user_id: str, user_manager: tuple[UserResponse, Manager] = Depends(get_current_active_user)):
    UsersViewSet.delete(user_id)

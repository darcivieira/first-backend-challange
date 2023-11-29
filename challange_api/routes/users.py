from fastapi import APIRouter, Depends
from challange_api.controllers.users import UsersViewSet
from challange_api.helpers.auth import get_current_active_user
from challange_api.serializers.users import UserResponse, UserCreate, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={
        404: {'description': 'NotFound'}
    }
)


@router.get("", response_model=list[UserResponse])
def list(user: UserResponse = Depends(get_current_active_user)):
    return UsersViewSet.list()


@router.post("", status_code=201, response_model=UserResponse)
def create(body: UserCreate):
    return UsersViewSet.create(body)


@router.get("/{user_id}", response_model=UserResponse)
def retrieve(user_id: str, user: UserResponse = Depends(get_current_active_user)):
    return UsersViewSet.retrieve(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def patch(user_id: str, body: UserUpdate, user: UserResponse = Depends(get_current_active_user)):
    return UsersViewSet.update(user_id, body)


@router.delete("/{user_id}", status_code=204, response_model=None)
def delete(user_id: str, user: UserResponse = Depends(get_current_active_user)):
    UsersViewSet.delete(user_id)

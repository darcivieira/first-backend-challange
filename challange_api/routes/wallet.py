from fastapi import APIRouter, Depends

from challange_api.controllers.wallet import WalletViewSet
from challange_api.generics.models import Manager
from challange_api.helpers.auth import get_current_active_user
from challange_api.serializers.users import UserResponse
from challange_api.serializers.wallet import WalletResponse, WalletUpdate

router = APIRouter(
    prefix="/wallets",
    tags=["Wallets"],
    responses={
        404: {'description': 'NotFound'}
    }
)


@router.get("/", response_model=WalletResponse)
def retrieve(user_manager: tuple[UserResponse, Manager] = Depends(get_current_active_user)):
    user, _ = user_manager
    return user.wallet


@router.patch("/", response_model=WalletResponse)
def patch(body: WalletUpdate, user_manager: tuple[UserResponse, Manager] = Depends(get_current_active_user)):
    user, _ = user_manager
    return WalletViewSet.update(user.wallet.id, body)

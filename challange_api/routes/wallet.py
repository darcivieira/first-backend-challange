from fastapi import APIRouter, Depends

from challange_api.controllers.wallet import WalletViewSet
from challange_api.generics.models import Manager
from challange_api.helpers.auth import get_current_active_user
from challange_api.serializers.users import UserResponse
from challange_api.serializers.wallet import WalletResponse, WalletUpdate
from challange_api.utils.dictionary import *

router = APIRouter(
    prefix="/wallets",
    tags=["Wallets"],
    responses={
        404: {'description': 'NotFound'}
    }
)


@router.get("/", response_model=WalletResponse, name=WALLET_RETRIEVE_NAME, description=WALLET_RETRIEVE_DESCRIPTION)
def retrieve(user_manager: tuple[UserResponse, Manager] = Depends(get_current_active_user)):
    """
    A method that return the user's wallet.

    Parameters:
        user_manager: A tuple with a user database instance and a manager instance

    Returns:
        An instance of pydantic data structure that represents the wallet default response body.
    """
    user, _ = user_manager
    return user.wallet


@router.patch("/", response_model=WalletResponse, name=WALLET_UPDATE_NAME, description=WALLET_UPDATE_DESCRIPTION)
def patch(body: WalletUpdate, user_manager: tuple[UserResponse, Manager] = Depends(get_current_active_user)):
    """
    A method that generate a wallet patch route.

    Parameters:
        body: An instance of pydantic data structure that represents the payload available to be updated.
        user_manager: A tuple with a user database instance and a manager instance

    Returns:
        An instance of pydantic data structure that represents the wallet default response body.
    """
    user, _ = user_manager
    return WalletViewSet.update(user.wallet.id, body)

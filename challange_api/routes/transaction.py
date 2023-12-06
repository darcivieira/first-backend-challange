from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from challange_api.controllers.transaction import TransactionViewSet
from challange_api.generics.models import Manager
from challange_api.helpers.auth import get_current_active_user
from challange_api.serializers.transaction import TransactionResponse, TransactionCreate, TransactionUpdate
from challange_api.serializers.users import UserResponse
from challange_api.utils.dictionary import *
from challange_api.utils.shortcuts import check_send_idempotency

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
    responses={
        404: {'description': 'NotFound'}
    }
)


@router.post("", status_code=201, response_model=TransactionResponse, name=TRANSACTION_CREATE_NAME, description=TRANSACTION_CREATE_DESCRIPTION)
def create(body: TransactionCreate, user_manager: tuple[UserResponse, Manager] = Depends(get_current_active_user)):
    """
    A method that allow you to generate one transaction.

    Parameters:
        body: An instance of pydantic data structure that represents the payload available to generate the transaction.
        user_manager: A tuple with a user database instance and a manager instance

    Returns:
        An instance of pydantic data structure that represents the transaction default response body.
    """
    user, _ = user_manager
    idempotency = check_send_idempotency(user.email, body.model_dump(exclude_unset=True), 'transaction')
    if idempotency:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This transaction already exist"
        )
    return TransactionViewSet.create(body, user_manager=user_manager)

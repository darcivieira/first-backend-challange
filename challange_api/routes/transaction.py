from fastapi import APIRouter, Depends
from challange_api.controllers.transaction import TransactionViewSet
from challange_api.helpers.auth import get_current_active_user
from challange_api.serializers.transaction import TransactionResponse, TransactionCreate, TransactionUpdate
from challange_api.serializers.users import UserResponse

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
    responses={
        404: {'description': 'NotFound'}
    }
)


@router.post("", status_code=201, response_model=TransactionResponse)
def create(body: TransactionCreate, user: UserResponse = Depends(get_current_active_user)):
    return TransactionViewSet.create(body, user=user)

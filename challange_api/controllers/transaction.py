from fastapi import HTTPException, status
from celery import current_app

from challange_api.generics.models import Manager
from challange_api.generics.viewsets import GenericViewSet
from challange_api.models import Transaction, Users
from challange_api.serializers.transaction import TransactionResponse, TransactionCreate, TransactionCreateInDB
from challange_api.serializers.users import UserResponse


class TransactionViewSet(GenericViewSet):
    query_session = Transaction.objects()
    response_serializer_class = TransactionResponse

    @staticmethod
    def get_valid_user(data: dict):
        sender, _ = data.get('user_manager')
        if not sender or sender.type == 'shopkeeper':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED if sender else status.HTTP_400_BAD_REQUEST,
                detail="This user in unauthorized" if sender else "BadRequest"
            )
        return sender

    @staticmethod
    def check_positive_balance_and_make_bank_draft(value: float, user_manager: tuple[UserResponse, Manager]):
        user, manager = user_manager
        if user.wallet.value < value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You don't have enough balance!"
            )
        user.wallet.value = float(user.wallet.value) - value
        manager.session.add(user)
        manager.session.commit()

    @staticmethod
    def get_receiver(register_number: str) -> UserResponse:
        return Users.objects().get(register_number=register_number)

    @classmethod
    def create(cls, body: TransactionCreate, **kwargs):
        sender = cls.get_valid_user(kwargs)
        cls.check_positive_balance_and_make_bank_draft(body.value, kwargs.get('user_manager'))
        receiver = cls.get_receiver(body.register_number)
        data = TransactionCreateInDB(**{"sender_id": sender.wallet.id, "receiver_id": receiver.wallet.id, "value": body.value})
        instance = cls.query_session.create(data)
        current_app.send_task("run_transaction", kwargs={"id": instance.id})
        return instance

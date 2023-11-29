from fastapi import HTTPException, status

from challange_api.generics.viewsets import GenericViewSet
from challange_api.models import Transaction, Users
from challange_api.serializers.transaction import TransactionResponse, TransactionCreate, TransactionCreateInDB


class TransactionViewSet(GenericViewSet):
    query_session = Transaction.objects()
    response_serializer_class = TransactionResponse

    @staticmethod
    def get_valid_user(data: dict):
        sender = data.get('user')
        if not sender or sender.type == 'shopkeeper':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED if sender else status.HTTP_400_BAD_REQUEST,
                detail="This user in unauthorized" if sender else "BadRequest"
            )
        return sender

    @classmethod
    def create(cls, body: TransactionCreate, **kwargs):
        sender = cls.get_valid_user(kwargs)
        receiver = Users.objects().get(register_number=body.register_number)
        data = TransactionCreateInDB(sender=sender.id, receiver=receiver.id)
        print(data)
        return cls.query_session.create(data)

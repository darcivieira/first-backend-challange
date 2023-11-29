from pydantic import BaseModel

from challange_api.generics.viewsets import GenericViewSet
from challange_api.models import Transaction
from challange_api.serializers.transaction import TransactionResponse


class TransactionViewSet(GenericViewSet):
    query_session = Transaction.objects()
    response_serializer_class = TransactionResponse

    @classmethod
    def create(cls, body: BaseModel):
        ...

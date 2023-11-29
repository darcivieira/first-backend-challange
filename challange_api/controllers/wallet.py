from challange_api.generics.viewsets import GenericViewSet
from challange_api.models import Wallet
from challange_api.serializers.wallet import WalletResponse


class WalletViewSet(GenericViewSet):
    query_session = Wallet.objects()
    response_serializer_class = WalletResponse

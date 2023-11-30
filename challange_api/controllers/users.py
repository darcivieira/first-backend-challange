from celery import current_app
from challange_api.generics.viewsets import GenericViewSet
from challange_api.serializers.users import UserResponse, UserCreate, UserUpdate, UserType
from challange_api.models.users import Users
from challange_api.models.wallet import Wallet
from challange_api.serializers.wallet import WalletCreate
from challange_api.utils.shortcuts import generate_hash


class UsersViewSet(GenericViewSet):
    query_session = Users.objects()
    response_serializer_class = UserResponse

    @classmethod
    def list(cls, *args, **kwargs):
        current_app.send_task("deploy_challange", kwargs={"data": "message"})
        return super().list(*args, **kwargs)

    @classmethod
    def create(cls, body: UserCreate):
        body.password = generate_hash(str(body.password.get_secret_value()))
        body.type = UserType.common.value if len(body.register_number) == 11 else UserType.shopkeeper.value
        data = cls.query_session.create(body)
        wallet_data = WalletCreate(user_id=data.id)
        Wallet.objects().create(wallet_data)
        return data

    @classmethod
    def update(cls, user_id: str, body: UserUpdate):
        instance = cls.query_session.get(id=user_id)
        if body.password:
            body.password = generate_hash(str(body.password))
        response = cls.query_session.update(instance, body)
        return response

from pydantic import BaseModel

from challange_api.generics.models import Manager
from challange_api.utils.shortcuts import get_object_or_404


class GenericViewSet:
    """
    This is a generic class that will provide the basic interaction between router's controllers,
    data serialization and database manager. So, you can customize your some methods to act as you
    need. To use it, you must set the query_session and response_serializer_class attributes.
    """
    query_session: Manager
    response_serializer_class: BaseModel

    @classmethod
    def list(cls, *args, **kwargs):
        return cls.query_session.all()

    @classmethod
    def create(cls, body: BaseModel):
        data = cls.query_session.create(body)
        return data

    @classmethod
    def retrieve(cls, pk: str):
        instance = get_object_or_404(cls.query_session, pk)
        cls.query_session.session.close()
        return instance

    @classmethod
    def update(cls, pk: str, body: BaseModel):
        instance = get_object_or_404(cls.query_session, pk)
        response = cls.query_session.update(instance, body)
        return response

    @classmethod
    def delete(cls, pk: str):
        instance = get_object_or_404(cls.query_session, pk)
        cls.query_session.delete(instance)

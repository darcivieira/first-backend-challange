import logging
from typing import TypeVar, Type

from challange_api.generics.models import Model, Manager
from challange_api.utils.exception import EmailNotSent
from challange_api.utils.shortcuts import make_request
from challange_api.models import Transaction, Wallet

T = TypeVar('T', bound=Model)
logger = logging.getLogger(__name__)


class MakeTransaction:

    @staticmethod
    def get_manager_session(model: Type[T]):
        return model.objects()

    @staticmethod
    def get_external_authorization():
        response = make_request("https://run.mocky.io/v3/5794d450-d2e2-4412-8131-73d0293ac1cc")
        if not isinstance(response, dict) or response.get('message') != 'Autorizado':
            return False
        return True

    @staticmethod
    def send_report(email: str):
        response = make_request(
            "https://run.mocky.io/v3/54dc2cf1-3add-45b5-b5a9-6bf7e7f1f4a6",
            request_type='POST',
            payload={"to": email, "message": "You received some money!"}
        )
        if not isinstance(response, dict) or not response.get('message'):
            raise EmailNotSent("The e-mail isn't sent")

    @staticmethod
    def commit_transaction_status_change(manager: Manager, transaction: Transaction, status: str):
        transaction.status = status
        if status == 'failed':
            transaction.sender.value = float(transaction.sender.value) + float(transaction.value)
        else:
            transaction.receiver.value = float(transaction.receiver.value) + float(transaction.value)
        manager.session.add(transaction)
        manager.session.commit()

    @classmethod
    def make_transaction_happens(cls, manager: Manager, transaction: Transaction):
        if cls.get_external_authorization():
            cls.commit_transaction_status_change(manager, transaction, 'success')
        else:
            cls.commit_transaction_status_change(manager, transaction, 'failed')

    @classmethod
    def run(cls, data: dict):
        manager = cls.get_manager_session(Transaction)
        transaction = manager.get(data.get('id'))

        if transaction.status == 'pending':
            cls.make_transaction_happens(manager, transaction)

        cls.send_report(transaction.receiver.user.email)

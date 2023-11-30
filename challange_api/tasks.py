from celery import shared_task

from challange_api.helpers.make_transaction import MakeTransaction
from challange_api.utils.exception import EmailNotSent


@shared_task(name="run_transaction", default_retry_delay=10, max_retries=2, autoretry_for=(EmailNotSent,))
def run_transaction(*args, **kwargs):
    MakeTransaction.run(kwargs)


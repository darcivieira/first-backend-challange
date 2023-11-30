import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="deploy_challange", default_retry_delay=2 * 60, max_retries=2)
def deploy(*args, **kwargs):
    logger.warning("Deploy world")
    logger.warning(args)
    logger.warning(kwargs)


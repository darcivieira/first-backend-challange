import pytest
from challange_api import tasks


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": "redis://127.0.0.1:6379/0",
        "result_backend": "redis://127.0.0.1:6379/0"
    }


@pytest.fixture(scope="session")
def celery_worker_parameters():
    return {"without_heartbeat": False}


@pytest.fixture(scope='session')
def celery_enable_logging():
    return True

import pytest
from challange_api import create_app
from fastapi.testclient import TestClient
from challange_api.generics.models import Model, engine
from challange_api.helpers.make_transaction import MakeTransaction

app = create_app()
celery = app.celery_app

client = TestClient(app)

USERS = [
        {
            "name": "José",
            "register_number": "12345678900",
            "email": "jose@gmail.com",
            "password": "a123@b987"
        },
        {
            "name": "Rodolfo",
            "register_number": "01234567890",
            "email": "rodolfo@yahoo.com",
            "password": "a123@b987"
        },
        {
            "name": "Empresa",
            "register_number": "12123456000189",
            "email": "financeiro@empresa.com",
            "password": "a123@b987"
        }
    ]

basic_data = {}

# pytest_plugins = ("celery.contrib.pytest", )


def create_users():
    Model.metadata.create_all(engine)
    for user in USERS:
        client.post('/users', json=user)


def test_first_common_user_authentication():
    create_users()
    payload = {'username': 'jose@gmail.com', 'password': 'a123@b987'}
    response = client.post('/token', json=payload)
    assert response.status_code == 200
    basic_data.update(
        {payload.get('username'): {'headers': {'Authorization': f'Bearer {response.json().get("access_token")}'}}}
    )


def test_second_common_user_authentication():
    create_users()
    payload = {'username': 'rodolfo@yahoo.com', 'password': 'a123@b987'}
    response = client.post('/token', json=payload)
    assert response.status_code == 200
    basic_data.update(
        {payload.get('username'): {'headers': {'Authorization': f'Bearer {response.json().get("access_token")}'}}}
    )


def test_shopkeeper_user_authentication():
    payload = {'username': 'financeiro@empresa.com', 'password': 'a123@b987'}
    response = client.post('/token', json=payload)
    assert response.status_code == 200
    basic_data.update(
        {payload.get('username'): {'headers': {'Authorization': f'Bearer {response.json().get("access_token")}'}}}
    )


def test_check_and_update_first_common_user_wallet():
    response = client.get('/wallets', headers=basic_data.get('jose@gmail.com').get('headers'))
    assert response.status_code == 200
    response = client.patch('/wallets', headers=basic_data.get('jose@gmail.com').get('headers'), json={"value": 1596.78})
    assert response.status_code == 200
    response = client.get('/wallets', headers=basic_data.get('jose@gmail.com').get('headers'))
    assert response.json().get('value') == 1596.78


@pytest.mark.celery(result_backend="rpc://")
def test_first_common_user_send_money_to_shopkeeper():
    response = client.post('/transactions', headers=basic_data.get('jose@gmail.com').get('headers'), json={"value": 156.0,"register_number": "12123456000189"})
    assert response.status_code == 201
    response = client.get('/wallets', headers=basic_data.get('jose@gmail.com').get('headers'))
    assert response.json().get('value') == 1440.78


@pytest.mark.celery(result_backend="rpc://")
def test_shopkeeper_user_send_money_to_shopkeeper():
    response = client.get('/wallets', headers=basic_data.get('financeiro@empresa.com').get('headers'))
    assert response.json().get('value') == 1440.78
    response = client.post('/transactions', headers=basic_data.get('financeiro@empresa.com').get('headers'), json={"value": 56.0,"register_number": "01234567890"})
    assert response.status_code == 401


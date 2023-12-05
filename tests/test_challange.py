from time import sleep
from challange_api import create_app
from fastapi.testclient import TestClient
from challange_api.generics.models import Model, engine

app = create_app()

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


def test_first_common_user_send_money_to_shopkeeper(celery_session_app, celery_session_worker):
    response = client.post('/transactions', headers=basic_data.get('jose@gmail.com').get('headers'), json={"value": 156.0,"register_number": "12123456000189"})
    assert response.status_code == 201
    response = client.get('/wallets', headers=basic_data.get('jose@gmail.com').get('headers'))
    assert response.json().get('value') == 1440.78


def test_shopkeeper_user_send_money_to_shopkeeper(celery_session_app, celery_session_worker):
    sleep(15)
    response = client.get('/wallets', headers=basic_data.get('financeiro@empresa.com').get('headers'))
    assert response.json().get('value') == 156.0
    response = client.post('/transactions', headers=basic_data.get('financeiro@empresa.com').get('headers'), json={"value": 56.0,"register_number": "01234567890"})
    assert response.status_code == 401


def test_second_common_user_send_money_to_shopkeeper(celery_session_app, celery_session_worker):
    sleep(15)
    response = client.get('/wallets', headers=basic_data.get('rodolfo@yahoo.com').get('headers'))
    assert response.json().get('value') == 0
    response = client.post('/transactions', headers=basic_data.get('rodolfo@yahoo.com').get('headers'), json={"value": 56.0,"register_number": "01234567890"})
    assert response.status_code == 401
    assert response.json() == {'detail': "You don't have enough balance!"}


def test_first_common_user_send_money_to_second_common_user(celery_session_app, celery_session_worker):
    sleep(15)
    response = client.post('/transactions', headers=basic_data.get('jose@gmail.com').get('headers'), json={"value": 555.55,"register_number": "01234567890"})
    assert response.status_code == 201


def test_second_common_user_send_money_to_shopkeeper_second_time(celery_session_app, celery_session_worker):
    sleep(15)
    response = client.post('/transactions', headers=basic_data.get('rodolfo@yahoo.com').get('headers'), json={"value": 50.0,"register_number": "12123456000189"})
    assert response.status_code == 201


def test_money_in_the_wallets():
    sleep(15)
    response = client.get('/wallets', headers=basic_data.get('jose@gmail.com').get('headers'))
    assert response.json().get('value') == 885.23
    response = client.get('/wallets', headers=basic_data.get('rodolfo@yahoo.com').get('headers'))
    assert response.json().get('value') == 505.55
    response = client.get('/wallets', headers=basic_data.get('financeiro@empresa.com').get('headers'))
    assert response.json().get('value') == 206.00



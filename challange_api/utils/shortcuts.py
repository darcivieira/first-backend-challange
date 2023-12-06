import base64
import json
import re
import requests
import uuid
import redis

from Crypto.Hash import SHA256
from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256
from challange_api.settings import settings


def uuid_url64():
    rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)


def generate_hash(secret: str):
    return pbkdf2_sha256.hash(secret)


def verify_password(secret: str, hash: str):
    return pbkdf2_sha256.verify(secret, hash)


def get_object_or_404(session, pk):
    instance = session.get(pk)
    if not instance:
        raise HTTPException(status_code=404, detail='Object not found!')
    return instance


def make_request(url: str, request_type: str = 'get', payload: dict = None) -> dict | bool:
    try:
        response = requests.request(request_type.upper(), url, data=payload)
    except Exception as err:
        return False
    else:
        return json.loads(response.content)


def encrypt_message(message):
    new_hash = SHA256.new()
    new_hash.update(message.encode('utf-8'))
    return base64.b64encode(new_hash.digest()).decode("utf-8")


def check_send_idempotency(email, data, value):
    key = encrypt_message(f"{email}-{data}")
    r = redis.Redis(host=settings.REDIS_HOST, port=6379)
    response = r.set(key, value, 30, get=True)
    return True if response else False


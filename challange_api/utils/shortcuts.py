import base64
import re
import uuid

from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256


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

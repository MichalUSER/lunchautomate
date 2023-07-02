from django.http import HttpRequest
from edupage_api import Edupage
from cryptography.fernet import Fernet
import base64
import logging
from django.conf import settings


class Request(HttpRequest):
    auth: Edupage


f = Fernet(settings.ENCRYPT_KEY)


def encrypt(password: str):
    encrypt_pass = f.encrypt(str.encode(password))
    return base64.urlsafe_b64encode(encrypt_pass)


def decrypt(password: bytes):
    password = base64.urlsafe_b64decode(password)
    return f.decrypt(password).decode("ascii")

from django.http import HttpRequest, HttpResponse
from edupage_api import Edupage


class Request(HttpRequest):
    auth: Edupage


def set_cookie(response: HttpResponse, key: str, value: str):
    response.set_cookie(key=key, value=value, samesite="None", secure=True)

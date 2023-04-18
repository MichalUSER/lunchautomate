from django.http.request import HttpRequest
from edupage_api import Edupage


class Request(HttpRequest):
    auth: Edupage

from django.http import HttpRequest, HttpResponse
from edupage_api import Edupage


class Request(HttpRequest):
    auth: Edupage

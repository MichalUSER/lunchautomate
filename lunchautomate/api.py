import orjson
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI, Form
from ninja.renderers import BaseRenderer
from edupage_api import Edupage, Lunch
from typing import Literal
from datetime import datetime
import time

from .schemas import UserIn
from .auth import GlobalAuth
from .types import Request



class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)


api = NinjaAPI(auth=GlobalAuth(), renderer=ORJSONRenderer())


@api.post("/authenticate", auth=None)
def authenticate(
    request: HttpRequest, response: HttpResponse, data: UserIn = Form(...)
):
    edupage = Edupage()
    edupage.login(data.username, data.password, "spsezoska")
    # response.set_cookie("username", data.username)
    # response.set_cookie("PHPSESSID", edupage.session.cookies.get(name="PHPSESSID"))
    return {
        "username": data.username,
        "token": edupage.session.cookies.get(name="PHPSESSID"),
    }


@api.get("/me")
def me(request: Request):
    return {"PHPSESSID": request.auth.session.cookies["PHPSESSID"]}


@api.get("/lunches")
def lunches(request: Request, date: float = time.time()):
    lunches = request.auth.get_lunches(datetime.fromtimestamp(date))
    if not isinstance(lunches, Lunch):
        return {"menus": {}}
    return {"menus": lunches.menus}

@api.get("/choose_lunch")
def choose_lunch(request: Request, date: float = time.time(), number: int = 1):
    lunches = request.auth.get_lunches(datetime.fromtimestamp(date))
    if number == 0:
        lunches.sign_off(request.auth)
    elif number > 3:
        return api.create_response(request, {"message": "Invalid lunch number"}, status=403)
    else:
        lunches.choose(request.auth, number)
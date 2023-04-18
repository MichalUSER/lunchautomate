import orjson
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI, Form
from ninja.renderers import BaseRenderer
from edupage_api import Edupage, Lunch

from .schemas import UserIn
from .auth import GlobalAuth
from .types import Request
from .custom_lunches import Lunches
from datetime import datetime, timedelta


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
def lunches(request: Request, date: str = ""):
    lunches = Lunches(request.auth).get_lunch(datetime.now() + timedelta(days=1))
    if not isinstance(lunches, Lunch):
        return {"menus": {}}
    return {"menus": lunches.menus}

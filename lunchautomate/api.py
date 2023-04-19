import orjson
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from ninja import NinjaAPI, Form
from ninja.renderers import BaseRenderer
from edupage_api import Edupage, Lunch
from datetime import datetime
import time

from .models import EdupageUser
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
    try:
        lunches = request.auth.get_lunches(datetime.fromtimestamp(date))
        if not isinstance(lunches, Lunch):
            return {"menus": {}}
        return {"menus": lunches.menus}
    except:
        return {"menus": {}}


@api.get("/choose_lunch")
def choose_lunch(request: Request, date: float = time.time(), number: int = 1):
    lunches = request.auth.get_lunches(datetime.fromtimestamp(date))
    if lunches is None:
        return api.create_response(
            request, {"message": "Error when fetching lunches"}, status=500
        )
    if number == 0:
        lunches.sign_off(request.auth)
    elif number > 8:
        return api.create_response(
            request, {"message": "Invalid lunch number"}, status=403
        )
    else:
        lunches.choose(request.auth, number)


@api.post("/add_lunch_cron", auth=None)
def add_lunch_cron(request, data: UserIn):
    try:
        edupage = Edupage()
        edupage.login(data.username, data.password, data.subdomain)
        user = EdupageUser(
            username=data.username, password=data.password, subdomain=data.subdomain
        )
        user.save()
    except Exception as e:
        print(e)
        return api.create_response(
            request, {"message": "Incorrect credentials"}, status=401
        )


@api.post("/remove_lunch_cron", auth=None)
def remove_lunch_cron(request, data: UserIn):
    try:
        edupage = Edupage()
        edupage.login(data.username, data.password, data.subdomain)
        user = EdupageUser.objects.get(username=data.username, subdomain=data.subdomain)
        user.delete()
    except:
        return api.create_response(
            request, {"message": "Incorrect credentials"}, status=401
        )

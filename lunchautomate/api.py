import orjson
import time
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer
from edupage_api import Edupage, Lunch
from datetime import datetime

from .models import EdupageUser
from .schemas import UserIn
from .auth import GlobalAuth
from .utils import Request, set_cookie


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)


api = NinjaAPI(auth=GlobalAuth(), renderer=ORJSONRenderer())


@api.post("/authenticate", auth=None)
def authenticate(request: HttpRequest, response: HttpResponse, data: UserIn):
    try:
        edupage = Edupage()
        edupage.login(data.username, data.password, data.subdomain)
        set_cookie(response, "username", data.username)
        set_cookie(
            response,
            "sessionId",
            edupage.session.cookies.get(name="PHPSESSID"),
        )
        set_cookie(response, "subdomain", data.subdomain)
    except Exception:
        return api.create_response(
            request, {"message": "Invalid credentials"}, status=401
        )


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
    try:
        lunches = request.auth.get_lunches(datetime.fromtimestamp(date))
    except:
        return api.create_response(
            request, {"message": "Lunch is not served on that date"}, status=500
        )
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


@api.get("/my_status")
def my_status(request: Request):
    exists = EdupageUser.objects.filter(
        username=request.auth.username, subdomain=request.auth.subdomain
    ).exists()
    return {"exists": exists}


@api.post("/add_lunch_cron", auth=None)
def add_lunch_cron(request, data: UserIn):
    try:
        edupage = Edupage()
        edupage.login(data.username, data.password, data.subdomain)
        user = EdupageUser(
            username=data.username.lower(),
            password=data.password,
            subdomain=data.subdomain.lower(),
        )
        user.save()
    except Exception:
        return api.create_response(
            request, {"message": "Invalid credentials"}, status=401
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
            request, {"message": "Invalid credentials"}, status=401
        )

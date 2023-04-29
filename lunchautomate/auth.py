from django.http import HttpRequest
from ninja.security import HttpBearer
from edupage_api import Edupage, Login


class GlobalAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token):
        edupage = Edupage()
        try:
            username = request.COOKIES["username"]
            subdomain = request.COOKIES["subdomain"]
            if len(username) == 0 or len(subdomain) == 0:
                raise
            Login(edupage).reload_data(subdomain, token, username)
            return edupage
        except:
            pass

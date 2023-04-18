from django.http import HttpRequest
from ninja.security import HttpBearer
from edupage_api import Edupage, Login


class GlobalAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token):
        edupage = Edupage()
        try:
            username = request.GET["username"]
            if len(username) == 0:
                raise
            Login(edupage).reload_data("spsezoska", token, username)
            return edupage
        except:
            pass

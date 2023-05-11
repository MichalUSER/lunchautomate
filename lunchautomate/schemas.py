from ninja import Schema


class UserIn(Schema):
    username: str
    password: str
    subdomain: str

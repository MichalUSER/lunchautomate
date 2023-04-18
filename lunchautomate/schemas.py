from ninja import Schema


class UserIn(Schema):
    username: str
    password: str


class UserOut(Schema):
    username: str
    token: str

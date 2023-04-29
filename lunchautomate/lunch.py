import orjson
from dataclasses import dataclass
from edupage_api.exceptions import FailedToChangeLunchError, InvalidLunchData
from edupage_api import EdupageModule
from datetime import datetime


def get_boarder_id(edupage: EdupageModule, date: datetime):
    date_strftime = date.strftime("%Y%m%d")
    request_url = f"https://{edupage.subdomain}.edupage.org/menu/?date={date_strftime}"
    response = edupage.session.get(request_url).content.decode()

    lunch_data = orjson.loads(response.split("edupageData: ")[1].split(",\r\n")[0])
    lunches_data = lunch_data.get(edupage.subdomain)

    try:
        boarder_id = lunches_data.get("novyListok").get("addInfo").get("stravnikid")
    except AttributeError as e:
        raise InvalidLunchData(f"Missing boarder id: {e}")

    return boarder_id


@dataclass
class Lunch:
    edupage: EdupageModule
    boarder_id: str

    def __make_choice(self, choice_str: str, date: datetime):
        request_url = f"https://{self.edupage.subdomain}.edupage.org/menu/"

        boarder_menu = {
            "stravnikid": self.boarder_id,
            "mysqlDate": date.strftime("%Y-%m-%d"),
            "jids": {"2": choice_str},
            "view": "pc_listok",
            "pravo": "Student",
        }

        data = {
            "akcia": "ulozJedlaStravnika",
            "jedlaStravnika": orjson.dumps(boarder_menu),
        }

        response = self.edupage.session.post(request_url, data=data).content.decode()

        if orjson.loads(response).get("error") != "":
            raise FailedToChangeLunchError()

    def choose(self, number: int, date: datetime):
        letters = "ABCDEFGH"
        letter = letters[number - 1]

        self.__make_choice(letter, date)

    def sign_off(self, date: datetime):
        self.__make_choice("AX", date)

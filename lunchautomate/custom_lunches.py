import orjson, re
from bs4 import BeautifulSoup, NavigableString
from edupage_api.module import EdupageModule, Module, ModuleHelper
from edupage_api.exceptions import (
    FailedToChangeLunchError,
    FailedToRateException,
    InvalidLunchData,
    NotLoggedInException,
)
from edupage_api.lunches import Lunch, Menu, Rating
from datetime import datetime


class Lunches(Module):
    @ModuleHelper.logged_in
    def get_lunch(self, date: datetime):
        date_strftime = date.strftime("%Y%m%d")
        request_url = (
            f"https://{self.edupage.subdomain}.edupage.org/menu/?date={date_strftime}"
        )
        response = self.edupage.session.get(request_url).content.decode()

        soup = BeautifulSoup(response, "html.parser")
        script = soup.find("script", string=re.compile("edupageData"))
        if (
            isinstance(script, NavigableString)
            or script is None
            or script.string is None
        ):
            raise TypeError("edupageData object not found")

        lines = script.string.split("\n")
        edupage_data_str = lines[20].strip()
        edupage_data_str_object = edupage_data_str[13:-1]
        lunch_data = orjson.loads(edupage_data_str_object)
        lunches_data = lunch_data.get(self.edupage.subdomain)

        try:
            boarder_id = lunches_data.get("novyListok").get("addInfo").get("stravnikid")
        except AttributeError as e:
            raise InvalidLunchData(f"Missing boarder id: {e}")

        lunch = lunches_data.get("novyListok").get(date.strftime("%Y-%m-%d"))

        if lunch is None:
            return None

        lunch = lunch.get("2")

        if lunch.get("isCooking") == False:
            return "Not cooking"

        served_from_str = lunch.get("vydaj_od")
        served_to_str = lunch.get("vydaj_do")

        if served_from_str:
            served_from = datetime.strptime(served_from_str, "%H:%M")
        else:
            served_from = None

        if served_to_str:
            served_to = datetime.strptime(served_to_str, "%H:%M")
        else:
            served_to = None

        title = lunch.get("nazov")

        amount_of_foods = lunch.get("druhov_jedal")
        chooseable_menus = list(lunch.get("choosableMenus").keys())

        can_be_changed_until = lunch.get("zmen_do")

        menus = []

        for food in lunch.get("rows"):
            if not food:
                continue

            name = food.get("nazov")
            allergens = food.get("alergenyStr")
            weight = food.get("hmotnostiStr")
            number = food.get("menusStr")
            rating = None

            if number is not None:
                number = number.replace(": ", "")
                rating = lunch.get("hodnotenia")
                if rating is not None and rating:
                    rating = rating.get(number)

                    [quality, quantity] = rating

                    quality_average = quality.get("priemer")
                    quality_ratings = quality.get("pocet")

                    quantity_average = quantity.get("priemer")
                    quantity_ratings = quantity.get("pocet")

                    rating = Rating(
                        date.strftime("%Y-%m-%d"),
                        boarder_id,
                        quality_average,
                        quantity_average,
                        quality_ratings,
                        quantity_ratings,
                    )
                else:
                    rating = None
            menus.append(Menu(name, allergens, weight, number, rating))

        return Lunch(
            served_from,
            served_to,
            amount_of_foods,
            chooseable_menus,
            can_be_changed_until,
            title,
            menus,
            date,
            boarder_id,
        )

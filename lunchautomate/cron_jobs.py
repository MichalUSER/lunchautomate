from time import sleep
from datetime import datetime, timedelta
from django_cron import CronJobBase, Schedule
from edupage_api import Edupage
from .models import EdupageUser
from .lunch import Lunch, get_boarder_id


def getDay(date: datetime, day: int) -> datetime:
    return date + timedelta(days=(day - date.weekday()) % 7)


def order_week(user: EdupageUser):
    date = getDay(datetime.now(), 0)
    edupage = Edupage()
    edupage.login(user.username, user.password, user.subdomain)
    boarder_id = get_boarder_id(edupage, date)
    lunch = Lunch(edupage, boarder_id)

    for _ in range(5):
        try:
            lunch.choose(1, date)
        except:
            pass
        date += timedelta(days=1)
        sleep(0.5)


class LunchCronJob(CronJobBase):
    RUN_WEEKLY_ON_DAYS = [5]
    RUN_AT_TIMES = ["12:00"]

    schedule = Schedule(run_on_days=RUN_WEEKLY_ON_DAYS, run_at_times=RUN_AT_TIMES)
    code = "lunchautomate.lunch_cron_job"

    def do(self):
        users = EdupageUser.objects.all()
        for user in users:
            order_week(user)

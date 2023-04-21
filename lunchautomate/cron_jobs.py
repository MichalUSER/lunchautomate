from django_cron import CronJobBase, Schedule
from .models import EdupageUser


class LunchCronJob(CronJobBase):
    RUN_WEEKLY_ON_DAYS = [6]
    RUN_AT_TIMES = ["12:00"]

    schedule = Schedule(run_on_days=RUN_WEEKLY_ON_DAYS, run_at_times=RUN_AT_TIMES)
    code = "lunchautomate.lunch_cron_job"

    def do(self):
        users = EdupageUser.objects.all()
        for user in users:
            print(user.username)

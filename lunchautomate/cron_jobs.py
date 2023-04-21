from django_cron import CronJobBase, Schedule
from .models import EdupageUser


class LunchCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "lunchautomate.lunch_cron_job"

    def do(self):
        users = EdupageUser.objects.all()
        for user in users:
            print(user.username)

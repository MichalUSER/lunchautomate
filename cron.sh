# Example crontab script - run at 12:00 on Saturday

0 12 * * 6 /path-to/venv/bin/python /path-to/lunchautomate/manage.py runcrons > /path-to/cronjob.log 2>&1

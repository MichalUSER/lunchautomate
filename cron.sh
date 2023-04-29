# Example crontab script - run every hour

0 * * * * /path-to/venv/bin/python /path-to/lunchautomate/manage.py runcrons > /path-to/cronjob.log 2>&1

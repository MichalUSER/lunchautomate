# Lunchautomate

Automate ordering lunches on edupage.

Built using python and django.

## Developing

Install dependencies, optionally in a python virtual environment

```
pip install -r requirements.txt
```

Run migrate commands

```
python manage.py migrate
python manage.py makemigrations
```

Create database tables

```
python manage.py migrate --run-syncdb
```

Run dev server

```
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.
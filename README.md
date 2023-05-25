# Lunchautomate API

Automate ordering lunches on edupage.

Built using python and django.

The web application lives [here](https://github.com/MichalUSER/lunchautomate-web)

## Developing

Install dependencies using [poetry](https://python-poetry.org)

```
poetry install
```

Activate venv

```
poetry shell
```

Run migrate commands

```
python manage.py migrate
python manage.py makemigrations
```

Create database tables (currently required)

```
python manage.py migrate --run-syncdb
```

Run dev server

```
python manage.py runserver
```

Open http://localhost:8000 in your browser.

# Lunchautomate API

Automate ordering lunches on edupage.

Built using python and django.

The web application lives [here](https://github.com/MichalUSER/lunchautomate-web)

## Developing

Set up env variables

```
cp .env.dev .env
```

Fill out variables in `.env` file

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

## Docker

Build the image

```
docker build .
```

Create and run a container

```
docker run -d -p 8000:8000 --name lunchautomate --env-file .env image_id
```

## Docker compose

Set `POSTGRES_HOST` in `.env.docker` to host ip, or `host.docker.internal`

Build compose images and run compose command

```bash
docker-compose up --build -d
```

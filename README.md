<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Description](#description)
- [Installation](#installation)
- [Running](#running)
	- [Starting dev server](#starting-dev-server)
	- [Application operations in `production` mode.](#application-operations-in-production-mode)
	- [Dependencies maintenance](#dependencies-maintenance)
	- [Running tests](#running-tests)
	- [Seeding database with fake development data](#seeding-database-with-fake-development-data)
	- [Application shell](#application-shell)
- [...](#)
	- [Application routes](#application-routes)
	- [Example of logging in and making requests](#example-of-logging-in-and-making-requests)

<!-- /TOC -->

# Description

Example Flask application with:
    - SQLAlchemy + PostgreSQL model layer
    - stateless JWT authentcation
    - REST API in view layer

Used as a teaching tool last year.

# Installation

See [INSTALL.md](INSTALL.md)

# Running

## Starting dev server

~~~
source .venv/bin/activate
python manage.py runserver
~~~

## Application operations in `production` mode.

- production mode looks for config file in following locations:
    - /etc/$(APPLICATION_NAME).conf
    - ~/$(APPLICATION_NAME).conf

- all operations available from `manage.py` are still available, but require
  stating `production` mode explicitly:

- note that it is still highly recommended to have all dependencies in virtual
  environment

~~~
source .venv/bin/activate
python manage.py --environment production runserver
~~~

For cron tasks, make sure application is started from its virtual environment:

~~~
4 2 * * * /home/app_user/app_name/.venv/bin/python /home/app_user/app_name/manage.py -e production my_fancy_task
~~~

## Dependencies maintenance

Add/remove packages from `requirements.in` and then:

~~~
source .venv/bin/activate
pip-compile requirements.in
pip install -r requirements.txt
~~~

## Running tests

~~~
source .venv/bin/activate
py.test
~~~

or, for spec output:

~~~
source .venv/bin/activate
py.test --spec
~~~

## Seeding database with fake development data

~~~
source .venv/bin/activate
python manage.py db truncate && python manage.py db upgrade && python manage.py db seed
~~~

Note that `seed` might sometimes fail on unique constraint violation. This is normal, just re-run above code until it passes

## Application shell

~~~
python manage.py shell
user = factories.UserFactory()
category = models.Category.query.first()
movies = category.movies()
# ...
~~~

## Application routes

~~~
source .venv/bin/activate
python manage.py routes
~~~

## Example of logging in and making requests

Make sure you'd ran `python manage.py db seed` because that will create test
user account. Than start dev server:

~~~
python manage.py runserver
~~~

1) Acquire JWT token:

Request:
~~~
POST /api/login HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "username_or_email": "test",
    "password": "test"
}
~~~

Response:
~~~
{
  "access_token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJ1c2VyX3JvbGVzIjpbInVzZXIiXSwiZXhwIjoxNDg0MjE1MzA1LCJ1c2VyX2lkIjoiMSJ9.8U9RgGGmwVgwBmY4PHjtOxp3HpnxGSSUro5uzFTouGj30J7lbJrXqQrSPvQmkQgnfiJ60PXaRVPKJTEurlCmoQ",
  "api_key": "b9f91d35da8607ca26346c453a36166cbcf7314c7b9589cd7393a3b79275627d",
  "expires_in": 86400,
  "token_type": "Bearer"
}
~~~

2) For any further requests, you must use JWT access_token acquired from `/api/login`. Ie, to get a list of movie categories:

Request:
~~~
GET /api/categories HTTP/1.1
Host: localhost:5000
Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJ1c2VyX3JvbGVzIjpbInVzZXIiXSwiZXhwIjoxNDg0MjE1MzA1LCJ1c2VyX2lkIjoiMSJ9.8U9RgGGmwVgwBmY4PHjtOxp3HpnxGSSUro5uzFTouGj30J7lbJrXqQrSPvQmkQgnfiJ60PXaRVPKJTEurlCmoQ
Cache-Control: no-cache
~~~

Response:
~~~
{
  "objects": [
    {
      "created_at": "2017-01-11T09:52:23+00:00",
      "id": 1,
      "name": "Action",
      "updated_at": "2017-01-11T09:52:23+00:00"
    },
    {
      "created_at": "2017-01-11T09:52:23+00:00",
      "id": 2,
      "name": "SciFi",
      "updated_at": "2017-01-11T09:52:23+00:00"
    },
    {
      "created_at": "2017-01-11T09:52:23+00:00",
      "id": 3,
      "name": "Horror",
      "updated_at": "2017-01-11T09:52:23+00:00"
    }
  ],
  "page": 1,
  "pages": 1,
  "per_page": 20,
  "total": 3
}
~~~

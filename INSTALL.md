# Install

Install instructions for development environments.

For more complex scenarions, it is usually good to idea to automate deployment
using Ansible...

## Preparing Python environment

0) Install system dependencies

~~~
$ sudo apt-get install build-essential git python3 python3-venv \
python3-dev libffi-dev postgresql-server-dev-all
~~~

1) prepare Python virtual environment

~~~
git clone ...
cd videostore
pyvenv .venv
source .venv/bin/activate
pip install -U pip pip-tools
deactivate
source .venv/bin/activate
pip-sync requirements.txt
~~~

## External services

### Database

Commands below produce database settings with weak, easy to guess passwords.
Do not use these in production!

0) Install PostgreSQL server

~~~
$ sudo apt-get install postgresql postgresql-contrib
~~~

1) Use PostgreSQL tools to create user, role and database

~~~
$ sudo -u postgres psql
postgres=# CREATE ROLE videostore LOGIN PASSWORD 'videostore' VALID UNTIL 'infinity';
postgres=# CREATE DATABASE videostore_dev WITH ENCODING='UTF8' OWNER=videostore CONNECTION LIMIT=-1;
postgres=# CREATE DATABASE videostore_test WITH ENCODING='UTF8' OWNER=videostore CONNECTION LIMIT=-1;
~~~

2) Edit settings (ie. database URI, secret key, etc...) in `development.conf`

~~~
sqlalchemy_uri = postgresql://videostore:videostore@localhost/videostore
~~~

4) Run database migrations:

~~~
source .venv/bin/activate
python manage.py db upgrade
~~~

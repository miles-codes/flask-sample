"""
Module to be used with WSGI containers.

Example:

using Gunicorn you can run the application indside of Gunicorn WSGI
container by issuing command:

gunicorn --bind my.foo.hostname:12345 videostore.wsgi:app
"""

from . import create_app

app = create_app('production')

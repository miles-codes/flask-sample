from flask.ext.sqlalchemy import SQLAlchemy
import logging

logger = logging.getLogger("videostore")

db = SQLAlchemy()

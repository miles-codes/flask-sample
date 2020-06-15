import time

from flask import current_app
from flask.ext.script import Command

from ..models import Movie


class MyFancyTask(Command):
    """Example of application specific task that can be run from ie. cron"""

    def run():
        current_app.logger.info("Started MyFancyTask...")

        # doing some really periodic important work
        time.sleep(2)

        current_app.logger.info("MyFancyTask sucessfully finished...")

from flask import Flask
from flask_restful import Api
from version import Version
from router import RequestRouter
from os import environ
from helpers import config_logger
import logging

logger = logging.getLogger("bbgc")

app = Flask(__name__)
api = Api(app, prefix='/api')

api.add_resource(Version, '/version')
api.add_resource(RequestRouter, '/bitbucket/invoke')


def validate_env():
    if "BBGC_SECRET_TOKEN" in environ:
        logger.info(
            "Running in secure mode.  Requests will be validated against secret token.")
    else:
        logger.warning(
            "Running in insecure mode.  Requests will not be validated against a webhook secret!")


# for running in gunicorn
if __name__ == 'server':
    config_logger(logging.INFO)
    validate_env()


if __name__ == '__main__':
    config_logger(logging.INFO)
    validate_env()
    app.run(host="0.0.0.0")

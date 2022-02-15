from flask_restful import Resource
from flask import request
import events
from os import environ
import hmac
import hashlib
import logging


logger = logging.getLogger("bbgc")


def not_implemented(event_key):
    logger.error("%s is not currently supported.", event_key)
    return {"Error": event_key + " is not currently supported."}, 400


def verify_signature(request_data):
    secret_token = environ.get('BBGC_SECRET_TOKEN')
    if secret_token is None:
        return True

    if not request.headers.get("X-Hub-Signature"):
        return False

    request_signature = request.headers.get("X-Hub-Signature").split("=")[1]
    digest = hmac.new(
        secret_token.encode("ascii"),
        request_data,
        hashlib.sha256).hexdigest()

    logger.debug("Request Signature: %s", request_signature)
    logger.debug("HMAC Digest: %s", digest)
    return digest == request_signature


class RequestRouter(Resource):
    def post(self):
        data = request.json
        raw_data = request.data

        if request.headers.get("X-Event-Key") == "diagnostics:ping":
            if "test" in data:
                return {"test": "successful"}, 200

        if not verify_signature(raw_data):
            logger.error("Request signatures do not match!")
            return {"error": "signature does not match"}, 401

        if "eventKey" not in data:
            logger.debug(
                "eventKey missing, not a valid bitbucket request: %s", data)
            return {"error": "not a valid bitbucket request"}, 400

        if data["eventKey"].startswith("mirror:"):
            not_implemented(data["eventKey"])

        return events.handle_event(data, request.args)

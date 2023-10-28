from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger

def handle_request():
    logger.debug("Initiated wait for headband connection process")
    return ["waiting for headband"]
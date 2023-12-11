from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger
from tools.headband import *

def handle_request():
    status = headband_is_connected()

    logger.debug("Checking Headband Connection")

    if status == True:
        return ["Connected"]

    return ["Not Connected"]
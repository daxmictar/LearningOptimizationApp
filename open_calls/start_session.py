from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json

from tools.logging import logger
from tools.session import * 

def handle_request():
    logger.debug("Requesting START_SESSION")

    refresh_session()

    try:
        start_session()
    except Exception as err:
        logger.debug(f"{err}")
        return INVALID_SESSION

    return START_SESSION
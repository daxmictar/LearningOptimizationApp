from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger
from tools.database.db_lib import refresh_db

def handle_request():
    logger.debug("Logging Out")
    refresh_db()
    return ["Logging Out"]
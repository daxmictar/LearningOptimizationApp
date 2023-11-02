from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger
from tools.database.db_lib import *

def handle_request():
    logger.debug("Refreshing Database")
    refresh_db()

    _,cur = get_db_instance()
    cur.execute("SELECT filename,watched FROM movies")
    logger.debug("List of (filename, watched) follows:")
    logger.debug(str(cur.fetchall()))

    return ["Refreshing Database"]
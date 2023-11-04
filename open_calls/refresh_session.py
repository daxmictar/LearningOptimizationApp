from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json

from tools.logging import logger
from tools.database.db_lib import *
from tools.session import *

REFRESH_DATABASE = ["Refreshing Database"]

def handle_request():
    logger.debug(REFRESH_DATABASE[0])
    refresh_db()

    logger.debug(REFRESH_SESSION[0])
    refresh_session()
    start_session()

    _, cur = get_db_instance()
    cur.execute("SELECT filename,watched FROM movies")
    logger.debug("List of (filename, watched) follows:")
    logger.debug(str(cur.fetchall()))

    return REFRESH_DATABASE
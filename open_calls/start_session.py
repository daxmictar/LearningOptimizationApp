from tools.logging import logger
from tools.session import * 

def handle_request():
    logger.debug("Requesting START_SESSION")

    refresh_session()

    try:
        start_session()
    except Exception as err:
        logger.debug(f"{err}")
        return [INVALID_SESSION]

    return [START_SESSION]

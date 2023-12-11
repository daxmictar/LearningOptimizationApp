from tools.logging import logger
from tools.session import *

def handle_request():
    logger.debug("Requesting END_SESSION")
    
    try:
        end_session()
    except Exception as err:
        logger.debug(f"{err}")
        return INVALID_SESSION

    session_time = calculate_session_time()
    set_session_duration(session_time)

    if session_time > 60.00 * 60.00:
        logger.debug(f"Elapsed time for session is {session_time / (60 * 60):.2f} hours")
    elif session_time > 60.00:
        logger.debug(f"Elapsed time for session is {session_time / 60:.2f} minutes")
    else:
        logger.debug(f"Elapsed time for session is {session_time:.2f} seconds")

    return END_SESSION

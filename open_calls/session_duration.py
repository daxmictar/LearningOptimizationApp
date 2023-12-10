from tools.logging import logger
from tools.session import *

def handle_request():
    global session_duration

    logger.debug("Requesting session duration")

    formatted_duration = f"{session_duration:.2f}"

    if session_duration > 60.00 * 60.00:
        formatted_duration = f"{formatted_duration / (60 * 60):.2f} hours"
        logger.debug(f"Retrieved time for session is {formatted_duration}")
    elif session_duration > 60.00:
        formatted_duration = f"{session_duration / 60:.2f} minutes"
        logger.debug(f"Retrieved time for session is {formatted_duration}")
    else:
        formatted_duration = f"{session_duration:.2f} seconds"
        logger.debug(f"Retrieved time for session is {formatted_duration}")
    
    return [str(formatted_duration)]

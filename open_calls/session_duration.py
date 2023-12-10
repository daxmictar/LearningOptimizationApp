from tools.logging import logger
from tools.session import *

def handle_request():
    global session_duration

    logger.debug("Requesting session duration")

    formatted_duration = f"{session_duration:0.2f}"
    
    return [str(formatted_duration)]

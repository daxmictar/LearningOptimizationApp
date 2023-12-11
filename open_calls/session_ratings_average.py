from tools.logging import logger
from tools.session import *

def handle_request():
    logger.debug("Requesting average of session ratings")
    
    avg = session_ratings_average()

    formatted_avg = f"{avg:0.2f}"

    return [formatted_avg]
from tools.database.db_lib import get_top_x_tags
from tools.logging import logger

def handle_request():
    logger.debug("Checking Headband Connection")
   
    tags = get_top_x_tags(5)
    
    return tags

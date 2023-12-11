from tools.database.db_lib import get_top_x_tags
from tools.logging import logger

TOP_X_TAGS = 5

def handle_request():
    logger.debug(f"Getting top {TOP_X_TAGS} watched tags from database")
   
    tags = get_top_x_tags(TOP_X_TAGS)
    
    return tags

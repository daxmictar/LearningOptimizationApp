from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger

from tools.attention import attention_handler, process_emotional_states

CLEAR_MESSAGE = "Attention Data Cleared"

def clear_data():
    attention_handler = None
    logger.log(f"{CLEAR_MESSAGE}")

def handle_request():
    clear_data()

    return [CLEAR_MESSAGE]
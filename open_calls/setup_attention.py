from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger

from tools.attention import attention_handler as handler, setup_emotions

def handle_request():
    global handler

    handler = attention.setup_emotions()

    return ["Attention Handler Initiated"]
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger

from tools.attention import stop_attention_capture, ATTENTION_ENDED

def handle_request():
    stop_attention_capture(True)

    return [ATTENTION_ENDED]
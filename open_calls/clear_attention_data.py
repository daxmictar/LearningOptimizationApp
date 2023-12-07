from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger

from tools.attention import reset_attention_data, ATTENTION_CLEARED

def handle_request():
    reset_attention_data(True)

    return [ATTENTION_CLEARED]
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger

from tools.attention import setup_emotions, ATTENTION_CREATED

def handle_request():
    setup_emotions(True)

    return [ATTENTION_CREATED]
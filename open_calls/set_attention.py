from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger
from tools.headband import *
from tools.attention import set_paid_attention

SET_ATTENTION = "Attention Set"

def handle_request(attention_value: float):

    set_paid_attention(attention_value, log=True)

    return [SET_ATTENTION]
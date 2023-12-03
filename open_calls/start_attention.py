from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger

import asyncio

from tools.attention import start_attention_capture, is_emotion_object_ready, ATTENTION_STARTED, ATTENTION_STARTED_ERROR

def handle_request():

    ready = is_emotion_object_ready()
        
    if ready:
        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(start_attention_capture(True))
        except Exception:
            logger.log("Bad Async Loop, check start_attention.py")
            return [ATTENTION_STARTED_ERROR]  
        finally:
            loop.close()

    return [ATTENTION_STARTED]

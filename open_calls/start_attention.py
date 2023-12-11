from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger

import asyncio

from tools.attention import start_attention_capture, is_emotion_object_ready, ATTENTION_STARTED, ATTENTION_STARTED_ERROR

def handle_request():
    ready = is_emotion_object_ready()

    if ready:        
        start_attention_capture(True)        

        return [ATTENTION_STARTED]

    return [ATTENTION_STARTED_ERROR]


# currently unused
def concurrent_collection_process():
    from tools.attention import start_attention_capture_conc

    ready = is_emotion_object_ready()

    if ready:
        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(start_attention_capture_conc(True))
        except Exception:
            logger.log("Bad Async Loop, check start_attention.py")
            return [ATTENTION_STARTED_ERROR]  
        finally:
            loop.close()
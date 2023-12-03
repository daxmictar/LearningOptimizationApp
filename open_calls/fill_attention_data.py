from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.logging import logger

from tools.attention import process_emotional_states, ATTENTION_FILLED

def handle_request():
    states = process_emotional_states(True)

    # TODO(Josh): fill in code here using the data collected from above
    # explanation here: https://sdk.brainbit.com/lib-emotions/ in Overview section

    # Inspect the process flow of the attention module to see what API calls must be made for 
    # process_mental_states to return useful output.

    # values for relative attention/relaxation to baseline from calibration
    relative_attention = states.rel_attention
    relative_relaxation = states.rel_relaxation

    # values for 'instantiate' attention/relaxation
    instantiate_attention = states.inst_attention
    instantiate_relaxation = states.inst_relaxation

    # -- start processing here -- 


    # -- end processing here --

    return [ATTENTION_FILLED]
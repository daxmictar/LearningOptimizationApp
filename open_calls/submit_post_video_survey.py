from flask import request, g, redirect                                                           
from tools.logging import logger
from neurosdk.cmn_types import * 

def handle_request(survey_data):
    logger.debug(survey_data)
    return ["Post Video Survey Submitted"]

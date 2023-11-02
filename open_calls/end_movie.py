from flask import request, g                                                                 
from tools.logging import logger   
from tools.headband import *
from neurosdk.cmn_types import * 

def handle_request(previous_video):
    #Send just the video name to the browser (May want to send more information later but for now working with this)
    return [previous_video]



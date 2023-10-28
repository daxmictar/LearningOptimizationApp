from flask import request, g, redirect, make_response                                                           

from neurosdk.cmn_types import * 
from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor

from tools.logging import logger   
from tools.headband import *


def handle_request():
    # Attempt a headband setup
    setup_callback()

    logger.debug(str(gl_scanner))

    return ["Begin headband initialization"]

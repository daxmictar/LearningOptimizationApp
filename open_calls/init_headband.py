from flask import request, g, redirect                                                           

from neurosdk.cmn_types import * 
from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor

from tools.logging import logger   
from tools.eeg import *


# Attempts to set up a connection with the headband
def setup_headband():
    logger.debug("Start scan")
    gl_scanner.start()


# Check if we have a connected headband
def headband_is_connected():
    return g.hb != None # (g.hb in g)


def handle_request():
    # Attempt a headband setup
    setup_headband()

    # TODO(DAX) create interactive step to find the proper headband after
    # the button has been pressed to initialize the headband

    # If we have a connected headband
    if headband_is_connected():
        return ["Headband Connected"]
    
    # If we do not have a connected headband
    return ["No Headband Connected"]

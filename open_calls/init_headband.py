from flask import request, g, redirect                                                           

from neurosdk.cmn_types import * 
from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor

from tools.logging import logger   
from tools.eeg import *

from app import headband


# Attempts to set up a connection with the headband
def setup_callback() -> None:
    logger.debug("Sensor Found Callback")
    gl_scanner.sensorsChanged = sensorFound


def start_headband_scanner() -> None:
    logger.debug("Start scan")
    gl_scanner.start()


# Check if we have a connected headband
def is_headband_connected() -> bool:
    logger.debug("Checking headband connection...")
    return headband != None
    #return g.hb != None # (g.hb in g)


def handle_request():
    # Attempt a headband setup
    setup_callback()

    start_headband_scanner()

    # used to be g.hb
    logger.debug(f"Current Headband State = {headband}")

    # If we have a connected headband
    if is_headband_connected():
        return ["Headband Connected"]
    
    # If we do not have a connected headband
    return ["No Headband Connected"]

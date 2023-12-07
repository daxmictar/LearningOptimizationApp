from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor
from neurosdk.brainbit_sensor import BrainBitSensor
from neurosdk.cmn_types import *

from tools.logging import logger

hb = None

""" 
    Utility interface for handling the headband 

    To work properly, headband_init_sensor must be called to pass the state
    of a Sensor object into this module.
"""

def headband_init_scanner() -> Scanner:
    """
        Initializes a scanner and a sensor object.
        This function should be called first. 

        Returns:
            A valid scanner object that scans for a BrainBit sensor
    """
    global hb

    scanner = Scanner([SensorFamily.SensorLEBrainBit])
    logger.debug(f"Created local headband scanner -> {scanner}")

    return scanner


def headband_init_sensor(sensor: Sensor) -> Sensor:
    """
        Passes an argument to the global headband variable.
        Initializes the global var by default but it must be 
        called before any other functions with hb as a dependency.

        Returns:
            The global sensor object.
    """
    global hb

    if sensor == None:
        hb = None
    else:
        hb = sensor

    return hb


def headband_is_connected() -> bool:
    """ 
    Checks headband connection status

        Returns:
            True if headband object exists
    """
    global hb

    logger.debug("Checking headband connection")
    check = False

    try:
        check = hb != None
    except:
        hb = None

    return check


def headband_start_signal() -> bool:
    """ 
        Starts the current headband signal to cause data
        to flow.

        Returns:
            True if a headband exists and could be started.
    """
    global hb

    if not headband_is_connected():
        logger.debug("No headband available to start")
        return False
    
    hb.exec_command(SensorCommand.CommandStartSignal)

    return True


def headband_stop_signal() -> bool:
    """ 
        Stops the current headband signal. 

        Returns:
            True if a headband exists and could be stopped.
    """
    global hb

    if not headband_is_connected():
        logger.debug("No headband available to stop")
        return False

    hb.exec_command(SensorCommand.CommandStopSignal)

    return True


def headband_get_sensor() -> Sensor:
    """
        Passes the state of the currently initialized sensor object, which 
        if connected, should be a Sensor object.
    """
    return hb

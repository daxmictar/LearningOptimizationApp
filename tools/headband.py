from tools.eeg import *
from tools.logging import logger

# utility interface for handling the headband

global hb
hb = None

logger.debug(f"headband handle initialized to {hb}")

# Attempts to set up a connection with the headband
def setup_callback() -> Scanner:
    """
        Initializes callback function to scan for headbands.
    """
    logger.debug("Assigning sensor found callback")
    gl_scanner.sensorsChanged = sensorFound

    return gl_scanner


def start_headband_scanner() -> None:
    """
        Starts a scan for any headbands. Deleting is handled
        by the callback function. Should be called after setup_callback().
    """
    logger.debug("Starting scan")
    gl_scanner.start()


def is_headband_connected() -> bool:
    """ 
    Checks headband connection status

        Returns:
            True if headband object exists
    """
    logger.debug("Checking headband connection")
    return hb != None


def start_headband_signal() -> bool:
    """ 
        Starts the current headband signal to cause data
        to flow.

        Returns:
            True if a headband exists and could be started.
    """
    if not is_headband_connected():
        logger.debug("No headband available to start")
        return False

    hb.exec_command(SensorCommand.CommandStartSignal)
    return True


def stop_headband_signal() -> None:
    """ 
        Stops the current headband signal. 

        Returns:
            True if a headband exists and could be stopped.
    """
    if not is_headband_connected():
        logger.debug("No headband available to start")
        return False

    hb.exec_command(SensorCommand.CommandStopSignal)
    return True


def get_head_band_sensor_object():
    return gl_sensor
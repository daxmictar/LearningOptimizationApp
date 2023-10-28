from tools.eeg import *
from tools.logging import logger

# utility interface for handling the headband

global hb
hb = None

logger.debug(f"headband handle initialized to {hb}")

def headband_setup() -> (Scanner, Sensor):
    """
        Initializes a scanner and a sensor object.
        This function should be called first. 

        Returns:
            A valid scanner object
    """
    logger.debug("Creating local headband scanner and sensor")
    scanner = Scanner([SensorFamily.SensorLEBrainBit])
    sensor = None

    return (scanner, sensor)


def headband_setup_callback() -> None:
    """
        Initializes callback function to scan for headbands.
    """
    if gl_scanner == None:
        logger.debug("No gl_scanner found")
        return

    logger.debug("Assigning sensor found callback")
    gl_scanner.sensorsChanged = sensorFound


def headband_start_scanner() -> None:
    """
        Starts a scan for any headbands. Deleting is handled
        by the callback function. Should be called after setup_callback().
    """
    logger.debug("Starting scan")
    gl_scanner.start()


def headband_is_connected() -> bool:
    """ 
    Checks headband connection status

        Returns:
            True if headband object exists
    """
    logger.debug("Checking headband connection")
    return hb != None


def headband_start_signal() -> bool:
    """ 
        Starts the current headband signal to cause data
        to flow.

        Returns:
            True if a headband exists and could be started.
    """
    if not headband_is_connected():
        logger.debug("No headband available to start")
        return False

    hb.exec_command(SensorCommand.CommandStartSignal)
    return True


def headband_stop_signal() -> None:
    """ 
        Stops the current headband signal. 

        Returns:
            True if a headband exists and could be stopped.
    """
    if not headband_is_connected():
        logger.debug("No headband available to start")
        return False

    hb.exec_command(SensorCommand.CommandStopSignal)
    return True


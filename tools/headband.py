from tools.eeg import *
from tools.logging import logger
from typing import Callable

# utility interface for handling the headband

logger.debug(f"headband handle initialized to {hb}")


def headband_init_scanner() -> Scanner:
    """
        Initializes a scanner and a sensor object.
        This function should be called first. 

        Returns:
            A valid scanner object that scans for a BrainBit sensor
    """
    logger.debug("Creating local headband scanner")

    scanner = Scanner([SensorFamily.SensorLEBrainBit])

    return scanner


def headband_init_sensor(sensor: Sensor) -> Sensor:
    """
        Passes an argument to the global headband variable.

        Returns:
            The global sensor object.
    """
    if sensor == None:
        logger.debug(f"Passed None to headband init")
        return None

    global hb

    hb: Sensor = sensor

    return hb


def headband_setup_callback(scanner: Scanner, callback: Callable[[Scanner, list[Sensor]]]) -> Scanner:
    """
        Initializes callback function to scan for headbands.

        Returns:
            The object with the callback added.
    """
    if scanner == None:
        logger.debug("Passed an empty scanner object as an argument")
        return

    logger.debug("Assigning sensor found callback")
    scanner.sensorsChanged = callback

    return scanner


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


def headband_stop_signal() -> bool:
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


def headband_get_sensor():
    return hb
from tools.eeg import *
from tools.logging import logger

global hb
hb = None

logger.debug(f"headband handle initialized to {hb}")

# Attempts to set up a connection with the headband
def setup_callback() -> None:
    logger.debug("Assigning sensor found callback")
    gl_scanner.sensorsChanged = sensorFound


def start_headband_scanner() -> None:
    logger.debug("Starting scan")
    gl_scanner.start()


# Check if we have a connected headband
def is_headband_connected() -> bool:
    logger.debug("Checking headband connection")
    return hb != None


def get_head_band_sensor_object():
    return gl_sensor
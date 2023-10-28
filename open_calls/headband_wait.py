from tools.logging import logger
from tools.headband import *
from time import sleep

def headband_status():
    # If we have a connected headband
    if headband_is_connected():
        return ["Headband Connected"]
    
    # If we do not have a connected headband
    return ["No Headband Connected"]

def temp_handle_request():
    """ for debug/testing purposes """
    seconds_to_wait = 10

    logger.debug(f"Initiated {seconds_to_wait} second wait for headband connection process")

    headband_start_scanner()

    sleep(seconds_to_wait)

    logger.debug(f"Waited for headband for {seconds_to_wait}")


def handle_request():
    temp_handle_request()
    
    return headband_status()
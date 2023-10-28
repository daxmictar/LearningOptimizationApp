from tools.logging import logger
from tools.headband import start_headband_scanner, is_headband_connected
from time import sleep

def headband_status():
    # If we have a connected headband
    if is_headband_connected():
        return ["Headband Connected"]
    
    # If we do not have a connected headband
    return ["No Headband Connected"]

def temp_handle_request():
    """ for debug/testing purposes """
    seconds_to_wait = 10

    logger.debug(f"Initiated {seconds_to_wait} second wait for headband connection process")

    start_headband_scanner()

    sleep(seconds_to_wait)

    logger.debug(f"Waited for headband for {seconds_to_wait}")


def handle_request():
    temp_handle_request()
    
    return headband_status()
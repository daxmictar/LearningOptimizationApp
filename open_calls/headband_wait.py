from tools.logging import logger
from tools.headband import *
from time import sleep
import concurrent.futures

def sensor_found_callback(scanner, sensors):
        for i in range(len(sensors)):
            print(f"Sensor found {sensors[i]}")


def headband_status():
    # If we have a connected headband
    if headband_is_connected():
        return ["Headband Connected"]
    
    # If we do not have a connected headband
    return ["No Headband Connected"]


def headband_connection_process():
    """ for debug/testing purposes """
    seconds_to_scan_for = 10

    # use wrapper function to create a new scanner
    scanner: Scanner = headband_init_scanner()

    # add a callback using wrapper function to show when a sensor has been found
    # it returns the same object passed as an argument but with the callback added
    scanner = headband_setup_callback(scanner, sensor_found_callback)

    # scan and wait for n seconds to fill the sensor list
    scanner.start()
    logger.debug(f"Initiated {seconds_to_scan_for} second wait for headband connection process")
    sleep(seconds_to_scan_for)
    logger.debug(f"Waited for {seconds_to_scan_for} seconds")
    scanner.stop()

    # use the scanner to create a sensor
    def connect_headband_sensor(info):
        return scanner.create_sensor(info)

    # go through each of the sensors acquired from the scan    
    sensor_info = scanner.sensors()
    sensor = None
    if len(sensor_info) > 0:
        for i in range(len(sensor_info)):
            current_sensor_info = sensor_info[i]
            logger.debug(f"Currently scanning {current_sensor_info}")

            with concurrent.futures.ThreadPoolExecutor() as exec:
                future = exec.submit(connect_headband_sensor, current_sensor_info)
                sensor = future.result()
            
    logger.debug(f"Sensor connection established {str(sensor)}")
    
    # get rid of the current scanner object
    # must redo this request to create a new scanner and reconnect
    logger.debug("Scanner process complete")
    del scanner

    headband_init_sensor(sensor)


def handle_request():
    headband_connection_process()
    
    return headband_status()
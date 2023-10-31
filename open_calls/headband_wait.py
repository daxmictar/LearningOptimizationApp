from tools.logging import logger
from tools.headband import *
from time import sleep
import concurrent.futures


def on_sensor_state_changed(sensor, state):
    logger.debug(f"object {sensor} named -> {sensor.name} is {state}")

def on_brain_bit_signal_data_received(sensor, data):
    # prints the current data object, which should be a BrainBitSensorInfo
    logger.debug(f"{data}\n")

def headband_connection_process():
    """ for debug/testing purposes """
    seconds_to_scan_for = 10

    # use wrapper function to create a new scanner
    scanner: Scanner = headband_init_scanner()
    logger.debug(f"Created headband scanner object {scanner}")

    # add a callback to show when a sensor has been found
    scanner.sensorsChanged = on_sensor_state_changed

    # scan and wait for n seconds to fill the sensor list
    scanner.start()
    logger.debug(f"Initiated {seconds_to_scan_for} second wait for headband connection process")
    sleep(seconds_to_scan_for)
    logger.debug(f"Waited for {seconds_to_scan_for} seconds")
    scanner.stop()

    # use the scanner to create a sensor
    def connect_headband_sensor(info):
        logger.debug(f"Creating sensor with {info}")
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
    else:
        num_sensors = len(sensor_info)
        logger.debug(f"No sensors found, sensors() list is {num_sensors}")
            
    # get rid of the current scanner object
    # must redo this request to create a new scanner and reconnect
    del scanner

    sensor = headband_init_sensor(sensor)

    if sensor != None:
        sensor.sensorStateChanged = on_sensor_state_changed
        sensor.connect()
        sensor.signalDataReceived = on_brain_bit_signal_data_received
        logger.debug(f"Sensor connection established {str(sensor)}")

    return sensor

def handle_request():
    sensor = headband_connection_process()

    if sensor != None:
        return ["Headband is connected"]
    
    return ["Headband is not connected"] 
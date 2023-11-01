from time import sleep

from tools.logging import logger
from tools.headband import *


def on_sensor_found(scanner, sensors):
    logger.debug(f"Using {scanner} to scan")
    for i in range(len(sensors)):
        logger.debug(f"Sensor found {sensors[i]}")


def on_sensor_state_changed(sensor, state):
    logger.debug(f"Sensor {sensor} is {state}")


def on_signal_data_received(sensor, data):
    # prints the current data object, which should be a BrainBitSensorInfo
    logger.debug(f"{data} from {sensor}\n")


def on_battery_changed(sensor, battery):
    logger.debug(f"Battery: {battery}%")


def headband_connection_process(seconds: float) -> Sensor | None:
    """ 
        Engages the headband connection process, which creates local scanner
        and scans for headbands. After the wait, scan through the list of all 
        sensors found. If there is a sensor object, connect to it and pass it
        to the global state of headband.py, from where it can be kept until 
        the current session is ended.

        Returns:
            A Sensor object if a connection has been made, otherwise None
    """
    scan_time = seconds

    # use wrapper function to create a new scanner
    scanner: Scanner = headband_init_scanner()

    # add a callback to show when a sensor has been found
    scanner.sensorsChanged = on_sensor_found

    # scan and wait for n seconds to fill the sensor list
    scanner.start()
    logger.debug(f"Initiated {scan_time} second wait for headband connection process")
    sleep(scan_time)
    logger.debug(f"Scanned for {scan_time} seconds")
    scanner.stop()

    # use the scanner to create a sensor
    def connect_headband_sensor(info):
        logger.debug(f"Creating sensor with {info}")
        return scanner.create_sensor(info)

    # go through each of the sensors acquired from the scan    
    sensors = scanner.sensors()
    num_sensors = len(sensors)
    logger.debug(f"sensors() list is size of {num_sensors}")

    sensor = None
    # list must have at least one sensor to attempt connection
    if len(sensors) > 0: 
        for i in range(len(sensors)):
            current_sensor = sensors[i]
            logger.debug(f"Currently scanning {current_sensor}")
            sensor = connect_headband_sensor(current_sensor) 
            
    # get rid of the current scanner object
    # must redo this request to create a new scanner and reconnect
    del scanner

    # pass the state of the sensor object to the headband.py module
    # and then pass it back, could be None OR a valid Sensor object
    sensor = headband_init_sensor(sensor)

    # if the object was successfully created, then assign relevant callbacks
    if sensor != None:
        logger.debug(f"Sensor connection established -> {str(sensor)}")
        sensor.sensorStateChanged = on_sensor_state_changed
        sensor.signalDataReceived = on_brain_bit_signal_data_received
        sensor.batteryChanged     = on_battery_changed

    return sensor

def handle_request():
    sensor = headband_connection_process(5.0)

    if sensor != None:
        return ["Headband is connected"]
    
    return ["Headband is not connected"] 
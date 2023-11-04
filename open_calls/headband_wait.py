from tools.logging import logger
from tools.headband import *

from time import sleep


gl_scanner = None
gl_sensor = None


def on_sensor_state_changed(sensor, state):
    logger.debug(f"object {sensor} named -> {sensor.name} is {state}")


def on_brain_bit_signal_data_received(sensor, data):
    # prints the current data object, which should be a BrainBitSensorInfo
    logger.debug(f"{data}\n")


def on_battery_changed(sensor, battery):
    logger.debug(f"{sensor.name} battery is now {battery}%")


# from Jardin's eeg.py
def sensor_found(scanner, sensors):
    global gl_scanner
    global gl_sensor
    for i in range(len(sensors)):
        logger.debug(f"Sensor -> {sensors[i]}")
        logger.debug("Connecting to sensor")
        gl_sensor = gl_scanner.create_sensor(sensors[i])
        gl_sensor.sensorStateChanged = on_sensor_state_changed
        gl_sensor.connect()
        gl_sensor.signalDataReceived = on_brain_bit_signal_data_received
        gl_sensor.batteryChanged = on_battery_changed
        gl_scanner.stop()
        del gl_scanner


def headband_connection_process():
    """ 
        Engages the headband connection process, which creates a module level scanner
        and scans for local headbands. Upon finding a headband, issue a callback which 
        creates a sensor object.
    """
    DELAY = 8.0

    # use utility function to create a scanner that just searches for the 
    # brainbit device that we want
    global gl_scanner
    global gl_sensor

    gl_scanner = headband_init_scanner()
    gl_sensor = None

    logger.debug("Added callback for sensorsChanged")
    # add a callback to show when a sensor has been found
    gl_scanner.sensorsChanged = sensor_found 
    gl_scanner.start()

    logger.debug("Begin delay for headband connection")

    while True:
        sleep(1)
        if gl_sensor != None:
            gl_sensor = headband_init_sensor(gl_sensor)
            break

    # creates a global var in the headband.py module which retains the state
    # of the newly created sensor object and then passes it back
    logger.debug(f"After {DELAY}, headband is {gl_sensor}")
    return gl_sensor

    
def handle_request():
    CONNECTED = ["Headband is connected"]
    NOT_CONNECTED = ["Headband is not connected"] 
    NO_BLUETOOTH = ["No valid bluetooth adapter"]

    sensor = None
    try:
        sensor = headband_connection_process()
    except Exception:
        return NO_BLUETOOTH

    if sensor != None:
        return CONNECTED
    
    return NOT_CONNECTED 
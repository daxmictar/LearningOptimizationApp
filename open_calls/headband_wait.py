from tools.logging import logger
from tools.headband import *

from time import sleep


def on_sensor_state_changed(sensor, state):
    logger.debug(f"object {sensor} named -> {sensor.name} is {state}")


def on_brain_bit_signal_data_received(sensor, data):
    # prints the current data object, which should be a BrainBitSensorInfo
    logger.debug(f"{data}\n")


def on_battery_changed(sensor, battery):
    logger.debug(f"{sensor.name} battery is now {battery}%")


def headband_connection_process():
    """ 
        Engages the headband connection process, which creates a module level scanner
        and scans for local headbands. Upon finding a headband, issue a callback which 
        creates a sensor object and passes it to the global state of headband.py, 
        from where it can be kept until the current session is ended.
    """
    DELAY = 5.0

    # use utility function to create a scanner that just searches for the 
    # brainbit device that we want
    gl_scanner = headband_init_scanner()
    gl_sensor = None

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

    logger.debug("Added callback for sensorsChanged")
    # add a callback to show when a sensor has been found
    gl_scanner.sensorsChanged = sensor_found 

    logger.debug("Begin delay for headband connection")
    sleep(DELAY)

    # creates a global var in the headband.py module which retains the state
    # of the newly created sensor object and then passes it back
    gl_sensor = headband_init_sensor(gl_sensor)
    logger.debug(f"After {DELAY}, headband is {gl_sensor}")

    return gl_sensor

    
def handle_request():
    sensor = headband_connection_process()

    if sensor != None:
        return ["Headband is connected"]
    
    return ["Headband is not connected"] 
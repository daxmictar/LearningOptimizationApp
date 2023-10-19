from neurosdk.scanner import Scanner
from neurosdk.sensor import Sensor
from neurosdk.brainbit_sensor import BrainBitSensor
from neurosdk.cmn_types import *

from tools.logging import logger   


#doing all this a the "module level" in "Demo" server mode it will work fine :)

def on_sensor_state_changed(sensor, state):
    logger.debug('Sensor {0} is {1}'.format(sensor.name, state))

def on_brain_bit_signal_data_received(sensor, data):
    from app import data_file

    #packnum1 = data[0].PackNum
    #marker1 = data[0].Marker
    #packet1_o1 = data[0].O1
    #packet1_o2 = data[0].O2
    #packet1_t3 = data[0].T3
    #packet1_t4 = data[0].T4

    #packnum2 = data[1].PackNum
    #marker2 = data[1].Marker
    #packet2_o1 = data[1].O1
    #packet2_o2 = data[1].O2
    #packet2_t3 = data[1].T3
    #packet2_t4 = data[1].T4

    #print(str(data) + '\n')

    data_file['file'].write(str(data) + '\n')

    #data_file['file'].write(f'{packnum1} {marker1} {packet1_o1} {packet1_o2} {packet1_t3} {packet1_t4}\n')
    #data_file['file'].write(f'{packnum2} {marker2} {packet2_o1} {packet2_o2} {packet2_t3} {packet2_t4}\n')

    #logger.debug(data)

logger.debug("Create Headband Scanner")
gl_scanner = Scanner([SensorFamily.SensorLEBrainBit])
gl_sensor = None
logger.debug("Sensor Found Callback")
def sensorFound(scanner, sensors):
    global gl_scanner
    global gl_sensor
    for i in range(len(sensors)):
        logger.debug('Sensor %s' % sensors[i])
        logger.debug('Connecting to sensor')
        gl_sensor = gl_scanner.create_sensor(sensors[i])
        gl_sensor.sensorStateChanged = on_sensor_state_changed
        gl_sensor.connect()
        gl_sensor.signalDataReceived = on_brain_bit_signal_data_received
        gl_scanner.stop()
        del gl_scanner

gl_scanner.sensorsChanged = sensorFound

logger.debug("Start scan")
gl_scanner.start()


def get_head_band_sensor_object():
    return gl_sensor


from tools.logging import logger
from tools.session import * 

from neurosdk.cmn_types import * 

from open_calls.headband_wait import gl_sensor


def on_brainbit_resist_data_received(sensor, data):
    print(data)


def handle_request():
    logger.debug("Requesting START_SESSION")

    refresh_session()

    logger.debug("Added a callback for resistance data")
    # callback for resistance data
    gl_sensor.resistDataReceived = on_brainbit_resist_data_received 

    gl_sensor.exec_command(SensorCommand.CommandStartResist)

    try:
        start_session()
    except Exception as err:
        logger.debug(f"{err}")
        return INVALID_SESSION

    return START_SESSION

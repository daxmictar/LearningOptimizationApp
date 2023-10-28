from flask import request, g                                                                 
from tools.logging import logger   
from tools.headband import *
from neurosdk.cmn_types import * 


def handle_request(video_name):
    from app import data_file

    #if g.hb == None:
    if not is_headband_connected():
        return ["No Headband"]

    #open file based on video name
    data_file['file'] = open(video_name + ".txt", "w")

    #Start signal to get data from headband
    #g.hb.exec_command(SensorCommand.CommandStartSignal)
    data_flow = start_headband_signal()

    logger.debug(f"Should data be flowing?: {data_flow}")

    return ["Data Flowing"]


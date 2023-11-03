from flask import request, g                                                                 
from tools.logging import logger   
from tools.headband import *
from neurosdk.cmn_types import * 

# using sensor from headband_wait due to callback
from open_calls.headband_wait import gl_sensor

def handle_request(video_name):
    from app import data_file

    if gl_sensor == None:
        return ["No Headband"]

    #open file based on video name
    data_file['file'] = open(video_name + ".txt", "w")

    gl_sensor.exec_command(SensorCommand.CommandStartSignal)

    return ["Data Flowing"]

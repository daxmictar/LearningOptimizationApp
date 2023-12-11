from flask import request, g                                                                 
from tools.logging import logger   
from tools.headband import *
from neurosdk.cmn_types import * 

# using sensor from headband_wait due to callback
from open_calls.headband_wait import gl_sensor

def get_next_video(previous_video: str):
    return previous_video

def handle_request(previous_video):
    from app import data_file
    
    #Place holder for finding next video
    next_video = get_next_video(previous_video)

    #If there is no headband we stop here
    if gl_sensor == None:
        #Send just the video name to the browser (May want to send more information later but for now working with this)
        return [next_video]

    #If there is a headband stop recieving data because no video is playing yet
    gl_sensor.exec_command(SensorCommand.CommandStopSignal)

    #close file based on video name
    data_file['file'].close()
    data_file['file'] = None

    #Send just the video name to the browser (May want to send more information later but for now working with this)
    return [next_video]

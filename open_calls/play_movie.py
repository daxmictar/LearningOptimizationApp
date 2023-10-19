from flask import request, g                                                                 
from tools.logging import logger   
from neurosdk.cmn_types import * 

def handle_request(video_name):
    from app import data_file

    if g.hb == None:
        #print("Data Flowing")
        return ["No Headband"]

    #open file based on video name
    data_file['file'] = open(video_name + ".txt", "w")

    #Start signal to get data from headband
    g.hb.exec_command(SensorCommand.CommandStartSignal)

    return ["Data Flowing"]


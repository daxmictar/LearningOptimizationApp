from flask import request, g                                                                 
from tools.logging import logger   
from neurosdk.cmn_types import * 


def handle_request(video_name):
    from app import data_file, headband
    logger.debug(f"headband from play_movie {headband}")

    #if g.hb == None:
    if headband == None:
        return ["No Headband"]

    #open file based on video name
    data_file['file'] = open(video_name + ".txt", "w")

    #Start signal to get data from headband
    #g.hb.exec_command(SensorCommand.CommandStartSignal)
    headband.exec_command(SensorCommand.CommandStartSignal)

    return ["Data Flowing"]


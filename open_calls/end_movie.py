from flask import request, g                                                                 
from tools.logging import logger   
from neurosdk.cmn_types import * 
import random
from db_test import set_watched, get_unwatched, get_tags

#Returns the next video based on the last video
#For now just randomly selects a unwatched video
#Next step is calculating a likely video based on watched videos tag history and video priority
def get_next_video(previous_video: str):
    #in db, set watched flag for previous video
    set_watched(previous_video)
    
    #get filename for next video
    next_video = get_unwatched(previous_video)

    return next_video


def handle_request(previous_video):
    from app import data_file
    
    #Place holder for finding next video
    next_video = get_next_video(previous_video)

    #Log out previous and next video
    logger.debug("Previous Video: " + previous_video + "\t" + "Next Video: " + next_video)

    #If there is no headband we stop here
    if g.hb == None:
        #Send just the video name to the browser (May want to send more information later but for now working with this)
        return [next_video]

    #If there is a headband stop recieving data because no video is playing yet
    g.hb.exec_command(SensorCommand.CommandStopSignal)

    #close file based on video name
    data_file['file'].close()
    data_file['file'] = None

    #Send just the video name to the browser (May want to send more information later but for now working with this)
    return [next_video]



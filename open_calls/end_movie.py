from flask import request, g                                                                 
from tools.logging import logger   
from neurosdk.cmn_types import * 
import random
from tools.database.db_lib import update_prev_get_next

#Returns the next video based on the last video
#Selection is based on the logic described by update_prev_get_next in db_lib.py
#Next step is calculating a likely video based on watched videos tag history and video priority
def get_next_video(previous_video: str):
    #change this value to affect how the following call of update_prev_get_next updates the watched value of previous video
    attention = random.getrandbits(1) #currently will set to 0 or 1 randomly

    #update value of watched for previous video based on value of attention, and get filename for next video
    next_video = (update_prev_get_next(previous_video, attention))

    return next_video


def handle_request(previous_video):
    from app import data_file, headband
    
    #Place holder for finding next video
    next_video = get_next_video(previous_video)

    #Log out previous and next video
    logger.debug("Previous Video: " + previous_video + "\t" + "Next Video: " + next_video)

    #If there is no headband we stop here
    # if g.hb == None:
    if headband == None:
        #Send just the video name to the browser (May want to send more information later but for now working with this)
        return [next_video]

    #If there is a headband stop recieving data because no video is playing yet
    # g.hb.exec_command(SensorCommand.CommandStopSignal)
    headband.exec_command(SensorCommand.CommandStopSignal)

    #close file based on video name
    data_file['file'].close()
    data_file['file'] = None

    #Send just the video name to the browser (May want to send more information later but for now working with this)
    return [next_video]



from flask import request, g                                                                 
from tools.logging import logger   
from tools.headband import *
from neurosdk.cmn_types import * 

def handle_request(previous_video):
    from app import data_file
    
    #Place holder for finding next video
    next_video = get_next_video(previous_video)

    #Log out previous and next video
    logger.debug("Previous Video: " + previous_video + "\t" + "Next Video: " + next_video)

    #If there is no headband we stop here
    if not headband_is_connected():
        #Send just the video name to the browser (May want to send more information later but for now working with this)
        return [next_video]

    #If there is a headband stop recieving data because no video is playing yet
    headband_stop_signal()

    #close file based on video name
    data_file['file'].close()
    data_file['file'] = None

    #Send just the video name to the browser (May want to send more information later but for now working with this)
    return [previous_video]



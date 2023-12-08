from flask import request, g                                                                 
from tools.logging import logger   
from tools.headband import *
from neurosdk.cmn_types import * 
import random
from tools.database.db_lib import update_prev_get_next, getval_watched

# using sensor from headband_wait due to callback
from open_calls.headband_wait import gl_sensor

#Returns the next video based on the last video
#Selection is based on the logic described by update_prev_get_next in db_lib.py
#Next step is calculating a likely video based on watched videos tag history and video priority
def get_next_video(previous_video: str):
    #change this value to affect how the following call of update_prev_get_next updates the watched value of previous video
    #currently sets to 0 or 1 randomly
    attention = random.getrandbits(1)

    #replace with call to get actual score from post video survey
    post_video_survey_score = random.randrange(1,5)

    #update value of watched for previous video based on value of attention, and get filename for next video
    next_video = (update_prev_get_next(previous_video, attention, post_video_survey_score))

    #check if the video that was just selected has already been watched
    #planning to move this check to within update_prev_get_next
    if getval_watched(next_video) == -1:
        next_video = "No Video"

    return next_video


def handle_request(previous_video, survey_info):
    from app import data_file
    from tools.attention import set_paid_attention, get_paid_attention

    print("Survey Info:")
    print(survey_info['AttentionRating'])
    print(survey_info['PreferenceRating'])

    set_paid_attention(survey_info['AttentionRating']/5)

    #Place holder for finding next video
    next_video = get_next_video(previous_video)

    #Log out previous and next video
    logger.debug("Previous Video: " + previous_video + "    Next Video: " + next_video)

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



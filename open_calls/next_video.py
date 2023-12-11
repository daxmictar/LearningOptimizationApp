from flask import request, g
from tools.logging import logger
from tools.headband import *
from neurosdk.cmn_types import *

# using sensor from headband_wait due to callback
from open_calls.headband_wait import gl_sensor

#Returns the next video based on the last video
#Selection is based on the logic described by update_prev_get_next in db_lib.py
def get_next_video(previous_video: str, attention_rating, preference_rating):
    from tools.database.db_lib import update_prev_get_next
    
    #update value of watched for previous video based on values of attention and preference rating, and get filename for next video
    next_video = (update_prev_get_next(previous_video, attention_rating, preference_rating))

    return next_video


def handle_request(previous_video, survey_info):
    from app import data_file
    from tools.attention import set_paid_attention, get_paid_attention

    set_paid_attention(float(survey_info['AttentionRating']))
    
    #Place holder for finding next video
    next_video = get_next_video(previous_video, get_paid_attention(), float(survey_info['PreferenceRating']))

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



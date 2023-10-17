from flask import request, g                                                                 
from tools.logging import logger   
from neurosdk.cmn_types import * 
import random
from db_test import set_watched

#Returns the next video based on the last video
#For now just randomly selects a unwatched video
#Next step is calculating a likely video based on watched videos tag history and video priority
def get_next_video(previous_video: str):
    #Next video to be returned
    next_video = ""

    #Remove the finished video from the list of unwatched videos (previous_video is just the name string)
    watched_video = g.unwatched_videos.pop(previous_video)
    set_watched(watched_video)

    #logger.debug(f"{watched_video}  {watched_video['name']}  {watched_video['tags']}")
    logger.debug(previous_video + " removed from unwatch list.")

    #Add the finished video to the list of watched videos 
    logger.debug(f"{g.unwatched_videos}")
    logger.debug(previous_video + " added to the watched list.")

    g.watched_videos.update({watched_video['name'] : watched_video})
    logger.debug(f"{g.watched_videos}")
    
    #Check if we have watched all the videos
    unwatched_keys = list(g.unwatched_videos.keys())
    #logger.debug(f"{unwatched_keys}")
    if(len(unwatched_keys) > 0):
        #Select a new video from the list of unwatched videos
        next_video = g.unwatched_videos[random.choice(unwatched_keys)]
        logger.debug(next_video['name'] + " selected as the next video to be played.")
    else:
        #Reload the previous video for now
        next_video = watched_video

    return next_video


def handle_request(previous_video):
    #Place holder for finding next video
    next_video = get_next_video(previous_video)

    #Log out previous and next video
    logger.debug("Previous Video: " + previous_video + "\n" + "Next Video: " + next_video['name'])

    #If there is no headband we stop here
    if g.hb == None:
        #Send just the video name to the browser (May want to send more information later but for now working with this)
        return [next_video['name']]

    #If there is a headband stop recieving data because no video is playing yet
    g.hb.exec_command(SensorCommand.CommandStopSignal)
    
    #Send just the video name to the browser (May want to send more information later but for now working with this)
    return [next_video['name']]



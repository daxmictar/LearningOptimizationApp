from flask import request, g, redirect                                                           
from tools.logging import logger   
from neurosdk.cmn_types import * 

#Attempts to set up a connection with the headband
def setup_headband():
    pass

#Check if we have a connected headband
def headband_is_connected():
    return True#(g.hb in g)

def handle_request():
    #Attempt a headband setup
    setup_headband()

    #If we have a connected headband
    if headband_is_connected():
        return ["Headband Connected"]
    
    #If we do not have a connected headband
    return ["No Headband Connected"]
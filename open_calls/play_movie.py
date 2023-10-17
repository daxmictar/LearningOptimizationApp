from flask import request, g                                                                 
from tools.logging import logger   
from neurosdk.cmn_types import * 

def handle_request():
    if g.hb == None:
        #print("Data Flowing")
        return ["No Headband"]

    g.hb.exec_command(SensorCommand.CommandStartSignal)


    return ["Data Flowing"]


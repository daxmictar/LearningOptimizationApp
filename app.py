from flask import Flask,render_template,request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import sys
import datetime
import bcrypt
import traceback

from tools.database.db_lib import refresh_db
from tools.token_required import token_required

#used if you want to store your secrets in the aws valut
#from tools.get_aws_secrets import get_secrets

from tools.logging import logger
from tools.headband import *
from tools.session import *

ERROR_MSG = "Ooops.. Didn't work!"

#Create our app
app = Flask(__name__)
#add in flask json
FlaskJSON(app)

global data_file
data_file = {"file" : None}

global usernames
usernames = {
    "test" : "test"
}

"""
#Set up watched videos
global watched_videos
watched_videos = {}

global unwatched_videos
unwatched_videos = {
    "movie.mp4" : {
        "name" : "movie.mp4",
        "tags" : ["Trees", "Bus", "Short"]
    },
    "movie1.mp4" : {
        "name" : "movie1.mp4",
        "tags" : ["Beach", "Person", "Water", "Medium"]
    },
    "movie2.mp4" : {
        "name" : "movie2.mp4",
        "tags" : ["Plants", "Bright", "Water", "Long"]
    },
    "movie3.mp4" : {
        "name" : "movie3.mp4",
        "tags" : ["Trees", "Plants", "Long"]
    }
}
"""

"""
#g is flask for a global var storage
def init_new_env():
    
    #To connect to DB
    if 'db' not in g:
        g.db = get_db()
    

    if headband == None:
        headband = get_head_band_sensor_object()
    
    #if 'hb' not in g:
    #    g.hb = get_head_band_sensor_object()

    #g.secrets = get_secrets()
    #g.sms_client = get_sms_client()
"""

#This gets executed by default by the browser if no page is specified
#So.. we redirect to the endpoint we want to load the base page
@app.route('/') #endpoint
def survey():
    return redirect('/static/log_in.html')


@app.route("/secure_api/<proc_name>",methods=['GET', 'POST'])
@token_required
def exec_secure_proc(proc_name):
    logger.debug(f"Secure Call to {proc_name}")
    
    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('secure_calls.'+proc_name), proc_name)
        resp = fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)
    
    print(resp)
    return resp


@app.route("/open_api/<proc_name>",methods=['GET', 'POST'])
def exec_proc(proc_name):
    logger.debug(f"Call to {proc_name}")
   
    #see if we can execute it..
    resp = ""
    try:
        fn = getattr(__import__('open_calls.' + proc_name), proc_name)
        
        

        #Check which proccess we are calling
        match(proc_name):
            case "end_movie":
                #For the end movie event we pass back {data : previous_video} 
                resp = fn.handle_request(request.form['data'])
            case "next_video":
                resp = fn.handle_request(request.form['data'], request.form)
            case "submit_survey" | "submit_post_video_survey" | "log_in":
                resp = fn.handle_request(request.form)
            case "play_movie":
                resp = fn.handle_request(request.form['data'])
            case _:
                #By default we pass nothing to the request
                resp = fn.handle_request()

    except Exception as err:
        ex_data = str(Exception) + '\n'
        ex_data = ex_data + str(err) + '\n'
        ex_data = ex_data + traceback.format_exc()
        logger.error(ex_data)
        return json_response(status_=500 ,data=ERROR_MSG)
    
    logger.debug(f"{resp}")

    return resp


if __name__ == '__main__':
    refresh_db()
    app.run(host='0.0.0.0', port=80)

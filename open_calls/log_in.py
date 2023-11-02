from flask import request, g                                                                 
from tools.logging import logger   
from tools.headband import *
from neurosdk.cmn_types import * 


def check_for_account(username):
    from app import usernames

    #(DATABASE REPLACE)
    if username in usernames.keys():
        return True

    return False

def check_password(username, password):
    from app import usernames

    #(DATABASE REPLACE)
    if password == usernames[username]:
        return True
    
    return False

def handle_request(form_response):
    from app import usernames

    username = form_response['username']
    password = form_response['password']

    if check_for_account(username):
        if check_password(username, password):
            return ["Correct Password"]
        else:
            return ["Wrong Password"]
        
    #Add the user to the usernames dict (DATABASE REPLACE)
    usernames[username] = password
    return ["User Not Found"]



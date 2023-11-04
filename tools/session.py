import time


from tools.session import *


session_start_time = 0.0
session_end_time = 0.0


# valid responses from API calls
INVALID_SESSION = ["No Session Started"]
REFRESH_SESSION = ["Refreshing Session"]
START_SESSION   = ["Start Session"]
END_SESSION     = ["End Session"]


# error messages
ERR_NO_CURRENT_SESSION  = "Session has not been started."
ERR_SESSION_IN_PROGRESS = "Session currently in progress."


class NoCurrentSession(Exception):
    def __init__(self, err_msg):
        self.value = err_msg

    def __str__(self):
        return repr(self.value)


class SessionInProgress(Exception):
    def __init__(self, err_msg):
        self.value = err_msg

    def __str__(self):
        return repr(self.value)


def start_session():
    """ 
        Starts the current login session, intended to be called on log in.

        :raise:
            SessionInProgress if called during an active session. 
    """
    global session_start_time

    if session_start_time > 0:
        raise SessionInProgress(ERR_SESSION_IN_PROGRESS)

    session_start_time = time.monotonic()


def end_session():
    """
        Ends the current login session, intended to be called on end_session

        :raise:
            NoCurrentSession if session_start_time is 0.
    """
    global session_start_time
    global session_end_time

    if session_start_time == 0:
        raise NoCurrentSession(ERR_NO_CURRENT_SESSION)

    session_end_time = time.monotonic()
    

def refresh_session():
    global session_start_time
    global session_end_time

    session_start_time = 0.0
    session_end_time = 0.0


def calculate_session_time():
    global session_start_time
    global session_end_time

    return session_end_time - session_start_time


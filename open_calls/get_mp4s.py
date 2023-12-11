import os

from tools.logging import *

def get_mp4s():
    target_dir = "static"
    
    files = [file for file in os.listdir(target_dir) if file.endswith(".mp4")]

    return files

def handle_request():
    logging.debug("Requesting MP4 files in static")

    mp4_files = get_mp4s()

    return mp4_files
import sqlite3
from db_con import get_db
from tools.logging import logger
from functools import reduce

"""
Name:       refresh_db
Purpose:    drop and recreate the movies table with default values
Parameter:  none
Return:     none
"""
def refresh_db():
    db = get_db()
    cur = db.cursor()

    #if movies table exists, drop it before (re)creation
    cur.execute("DROP TABLE IF EXISTS movies")

    #create movies table
    cur.execute("CREATE TABLE movies (filename TEXT PRIMARY KEY, tags TEXT, watched INTEGER)")
    """
    key for attribute 'watched':
         -1 : watched with attention
          0 : unwatched (initial default)
        >=1 : watched partially or without attention, where value equals quantity of failures to watch with attention
    """

    #insert rows descriptive of movies located in static directory
    cur.execute("INSERT INTO movies VALUES ('movie.mp4', 'Trees Bus Short', 0)")
    cur.execute("INSERT INTO movies VALUES ('movie1.mp4', 'Beach Person Water Medium', 0)")
    cur.execute("INSERT INTO movies VALUES ('movie2.mp4', 'Plants Bright Water Long', 0)")
    cur.execute("INSERT INTO movies VALUES ('movie3.mp4', 'Trees Plants Long', 0)")

    db.commit()
    db.close()
    
"""
Name:       is_watched
Purpose:    get the value of the watched attribute for the video with passed filename
Parameter:  string representing video filename
Return:     integer representing value of watched attribute
"""
def is_watched(movie):
    db = get_db()
    cur = db.cursor()
    
    cur.execute("SELECT watched FROM movies WHERE filename=?", (movie,))
    watched = cur.fetchone()[0]
    
    db.close()
    
    return watched

"""
Name:       set_watched
Purpose:    set the watched flag of the video with passed filename to -1
Parameter:  string representing video filename
Return:     none
"""
def set_watched(movie):
    db = get_db()
    cur = db.cursor()

    #if watched flag is not already set on video with passed string as filename...
    cur.execute("SELECT watched FROM movies WHERE filename=?", (movie,))
    if cur.fetchone()!=(-1,):
        logger.debug("Setting watched flag for " + movie)

        #set watched flag of video with passed filename to -1
        cur.execute("UPDATE movies SET watched=-1 WHERE filename=?", (movie,))

    db.commit()

    #debug messages
    logger.debug("Unwatched videos:")
    cur.execute("SELECT filename FROM movies WHERE watched=0")
    logger.debug(str(cur.fetchall()))
    logger.debug("Watched videos:")
    cur.execute("SELECT filename FROM movies WHERE watched=-1")
    logger.debug(str(cur.fetchall()))

    db.close()

"""
Name:       get_unwatched
Purpose:    get the filename of a random unwatched video
Parameter:  string representing video filename
Return:     string representing video filename
"""
def get_unwatched(previous_video):
    db = get_db()
    cur = db.cursor()

    #if there are any more unwatched videos, set next_video to the filename of a random unwatched video and return it
    cur.execute("SELECT COUNT(*) FROM movies WHERE watched=0")
    if cur.fetchone()[0]>0:
        cur.execute("SELECT filename FROM movies WHERE watched=0 ORDER BY random()") 
        next_video = cur.fetchone()[0]
        db.close()

        logger.debug("Randomly selecting an unwatched video.")

        return next_video
    
    #if no more unwatched videos, return the passed string (previous video filename)
    else:
        db.close()
        logger.debug("No unwatched videos remain. Replaying previous.")
        return previous_video
    
"""
Name:       get_tags
Purpose:    get list of tags for video with passed filename
Parameter:  string representing video filename
Return:     list of strings representing tags
"""
def get_tags(movie):
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT tags FROM movies WHERE filename=?", (movie,))
    #split the result of the above query (string delimited by spaces) into a list of strings
    tag_list = (cur.fetchone()[0]).split()

    db.close()

    return tag_list

"""
Name:       get_matching_videos
Purpose:    get a list of video filenames which match all of the tags in the passed list of tags
            (currently does not discriminate by watched attribute value)
Parameter:  list of strings representing tags
Return:     list of strings representing video filenames
"""
def get_matching_videos(tag_list):
    db = get_db()
    cur = db.cursor()
    
    #initiate list of lists, where each list contains the results of a query for one tag
    superlist = []
    
    #iterate through passed list
    for tag in tag_list:
        #query for list of filenames for videos which have the current tag
        cur.execute("SELECT filename FROM movies WHERE (INSTR(tags, ?))>0", (tag,))
        
        #append list from above query to superlist
        superlist.append(cur.fetchall())
        
    db.close()
    
    #create new list which contains only common elements (filenames) between all lists in superlist
    match_list = list(reduce(lambda i, j: i & j, (set(x) for x in superlist)))
    
    return match_list
import sqlite3
from tools.logging import logger
from functools import reduce

"""
Name:       get_db
Purpose:    Create and return a sqlite3 database connection.
Parameter:  none
Return:     sqlite.Connection
"""
def get_db():
    return sqlite3.connect("local_data_base")

"""
Name:       get_db_instance
Purpose:    Create and return a sqlite3 database connection and a cursor for the connection to facilitate querying.
Parameter:  none
Return:     sqlite3.Connection, sqlite3.Cursor
"""
def get_db_instance():  
    db  = get_db()
    cur  = db.cursor()
    return db, cur 

"""
Name:       refresh_db
Purpose:    Drop and recreate the movies table with default values.
Parameter:  none
Return:     none
"""
def refresh_db():
    db, cur = get_db_instance()

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
Name:       getval_watched
Purpose:    Get the value of the watched attribute for the video with passed filename. 
            If no video with passed filename found, return -2.
Parameter:  STRING representing video filename
Return:     INTEGER representing value of watched attribute
"""
def getval_watched(movie):
    db, cur = get_db_instance()
    
    cur.execute("SELECT watched FROM movies WHERE filename=?", (movie,))
    temp = cur.fetchone()

    if temp is None:
        watched = -2
    else:
        watched = temp[0]
    
    db.close()
    
    return watched

def update_watched(previous_video, attention):
    db, cur = get_db_instance()

    #if attention flag is 1, set the watched value of video with passed filename to -1
    if attention==1:
        cur.execute("UPDATE movies SET watched=-1 WHERE filename=?", (previous_video,))
    #else increment its watched value by 1
    else:
        cur.execute("UPDATE movies SET watched=watched+1 WHERE filename=?", (previous_video,))

    #debug output
    cur.execute("SELECT filename, watched FROM movies")
    logger.debug("List of (filename, watched):    %s", str(cur.fetchall()))

    db.commit()
    db.close()
    
"""
Name:       get_tags
Purpose:    Get list of tags for video with passed filename.
Parameter:  STRING representing video filename
Return:     LIST OF STRINGS representing tags
"""
def get_tags(movie):
    db, cur = get_db_instance()

    cur.execute("SELECT tags FROM movies WHERE filename=?", (movie,))
    #split the result of the above query (string delimited by spaces) into a list of strings
    tag_list = (cur.fetchone()[0]).split()

    db.close()

    return tag_list

"""
Name:       get_matching_videos
Purpose:    Get a list of video filenames which match all of the tags in the passed list of tags.
            (currently does not discriminate by watched attribute value)
Parameter:  LIST OF STRINGS representing tags
Return:     LIST OF STRINGS representing video filenames
"""
def get_matching_videos(tag_list):
    db, cur = get_db_instance()
    
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

def get_next_ignore_tags(previous_video, attention):
    db, cur = get_db_instance()
    
    #query and store the filename of the movie with the lowest non-negative watched value (tie goes to "lowest" filename)
    cur.execute("SELECT filename FROM movies WHERE watched=(SELECT MIN(watched) FROM movies WHERE watched>-1) LIMIT 1")
    temp = cur.fetchone()

    #if the above query got no hits (all videos have been watched with attention), replay the previous video
    if temp is None:
        next_video=previous_video
    #else will return the filename produced by the query
    else:
        next_video = temp[0]

    db.close()

    return next_video

def fts_create_and_copy():
    db, cur = get_db_instance()

    cur.execute("CREATE VIRTUAL TABLE movies_fts USING fts5 (filename, tags, watched)")
    cur.execute("INSERT INTO movies_fts (filename, tags, watched) SELECT filename, tags, watched FROM movies WHERE watched>-1")

    db.commit()
    db.close()

def update_prev_filter_next(previous_video, attention, tag_list):
    update_watched(previous_video, attention)

    db, cur = get_db_instance()

    cur.execute("SELECT COUNT(*) FROM movies WHERE watched>-1")
    if cur.fetchone()==0:
        

    if not tag_list:
        return get_next_ignore_tags(previous_video, attention)

    else:
        joined_tags = ' AND '.join(tag_list)

        fts_create_and_copy()
        cur.execute("SELECT filename FROM movies_fts WHERE watched=(SELECT MIN(watched) FROM movies WHERE watched>-1) AND tags MATCH '?'", joined_tags)
        temp = cur.fetchone()

        if temp is not None:
            return temp
        else:
            while temp is None and tag_list:
                cur.execute("SELECT filename FROM movies_fts WHERE watched>-1 AND tags MATCH '?'", joined_tags)
                temp = cur.fetchone()
                
        cur.execute("DROP TABLE IF EXISTS movies_fts")
        
        db.commit()
    
    db.close()

"""
Name:       set_watched
Purpose:    NOTICE: This function is effectively subsumed by update_prev_get_next
            Set the watched flag of the video with passed filename to -1.
Parameter:  STRING representing video filename
Return:     none
"""
"""
def set_watched(movie):
    db, cur = get_db_instance()

    #if watched flag is not already set on video with passed string as filename...
    cur.execute("SELECT watched FROM movies WHERE filename=?", (movie,))
    if cur.fetchone()!=(-1,):
        logger.debug("Setting watched flag for " + movie)

        #set watched flag of video with passed filename to -1
        cur.execute("UPDATE movies SET watched=-1 WHERE filename=?", (movie,))

    db.commit()
    db.close()
"""

"""
Name:       get_unwatched
Purpose:    NOTICE: This function is effectively subsumed by update_prev_get_next
            Get the filename of a random unwatched video.
Parameter:  STRING representing video filename
Return:     STRING representing video filename
"""
"""
def get_unwatched(previous_video):
    db, cur = get_db_instance()

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
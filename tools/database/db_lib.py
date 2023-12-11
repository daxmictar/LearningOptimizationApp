import sqlite3
import json
from tools.logging import logger

num_tags = 0

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
Name:       set_all_watched
Purpose:    Set the watched attribute for all rows in movies to -1 (watched with attention)
Parameter:  none
Return:     none
"""  
def set_all_watched():
    db, cur = get_db_instance()
    
    cur.execute("UPDATE movies SET watched=-1")

    db.commit()
    db.close()

"""
Name:       reset_all_watched
Purpose:    Update the watched attribute value of all rows in movies table to 0 (unwatched)
Parameter:  none
Return:     none
"""
def reset_all_watched():
    db, cur = get_db_instance()

    cur.execute("UPDATE movies SET watched=0")

    db.commit()
    db.close()

"""
Name:       count_unwatched
Purpose:    Return an integer representing the number of movies which have watched > -1.
Parameter:  none
Return:     INTEGER representing number of movies with watched > -1
"""
def count_unwatched():
    db, cur = get_db_instance()

    cur.execute("SELECT COUNT(*) FROM movies WHERE watched>-1")
    count = cur.fetchone()[0]

    db.close()

    return count

"""
Name:       refresh_db
Purpose:    Drop and recreate the movies table with default values
Parameter:  none
Return:     none
INFO:       movies/watched:
                -1  = watched with attention
                0   = unwatched (default)
                >0 = watched partially or without attention, where value equals quantity of failures to watch with attention
            tags/weight:
                float in range [0,1] where higher reflects more 'educational relevance'
            tags/favor:
                float in range [1,39] adjusted according to user review and attention during movie
"""
def refresh_db():
    global num_tags
    
    db, cur = get_db_instance()

    #if tables exist, drop before (re)creation
    cur.execute("DROP TABLE movies")
    cur.execute("DROP TABLE tags")

    #create tables
    cur.execute("CREATE TABLE movies (id INTEGER PRIMARY KEY, filename TEXT NOT NULL, tags TEXT NOT NULL, watched INTEGER NOT NULL)")
    cur.execute("CREATE TABLE tags (name TEXT PRIMARY KEY, weight REAL, favor REAL)")

    f = open("tools/database/updated_movies.json") #open file movies.json
    dict_list = json.load(f) #create list of dict objects from json file

    movie_id = 0 #initialize counter to assign id primary key to movies
    
    #initialize attributes which have a common default for all rows
    default_watched = 0
    default_favor = 20

    #loop through list, inserting an entry into movies table for each dictionary object
    for movie in dict_list:
        cur.execute("INSERT INTO movies VALUES (?, ?, ?, ?)", (movie_id, movie["filename"], movie["tags"], default_watched))
        movie_id += 1

    f = open("tools/database/updated_tags.json") #open file tags.json
    dict_list = json.load(f) #create list of dict objects from json file

    #loop through list, inserting an entry into tags table for each dictionary object
    for tag in dict_list:
        cur.execute("INSERT INTO tags VALUES (?, ?, ?)", (tag["name"], tag["weight"], default_favor))
        num_tags += 1

    f.close() #close file

    db.commit()
    db.close()

"""
Name:       fts_create_and_copy
Purpose:    Create a virtual movies table and copy all rows from its physical counterpart.
Parameter:  none
Return:     none
"""
def fts_create_and_copy():
    db, cur = get_db_instance()

    cur.execute("DROP TABLE IF EXISTS movies_fts")

    cur.execute("CREATE VIRTUAL TABLE movies_fts USING fts5 (filename, tags, watched)")
    cur.execute("INSERT INTO movies_fts (filename, tags, watched) SELECT filename, tags, watched FROM movies WHERE watched>-1")

    db.commit()
    db.close()
    
"""
Name:       getval_watched
Purpose:    Get the value of the watched attribute for the video with passed filename. 
            If no video with passed filename found, return -2.
Parameter:  STRING representing video filename
Return:     INTEGER representing value of watched attribute
"""
def getval_watched(filename):
    db, cur = get_db_instance()
    
    #query for watched value of movie with passed filename
    cur.execute("SELECT watched FROM movies WHERE filename=?", (filename,))
    temp = cur.fetchone()

    #if query got no hits (probably invalid movie name), will return -2
    if temp is None:
        watched = -2

    #if query got a hit, will return it
    else:
        watched = temp[0]
    
    db.close()
    
    return watched

"""
Name:       update_watched
Purpose:    Update the watched attribute value of the movie with passed filename based on passed attention value.
            Attention < 5.0 will cause watched to be incremented by 1. Attention == 5.0 will cause watched to get -1.
Parameter:  STRING representing video filename, 
            FLOAT [1,5] representing user's level of attention
Return:     none
"""
def update_watched(previous_video, attention):
    db, cur = get_db_instance()

    #if attention value is 5.0, set the watched value of video with passed filename to -1
    if attention==5.0:
        cur.execute("UPDATE movies SET watched=-1 WHERE filename=?", (previous_video,))
    #else increment its watched value by 1
    else:
        cur.execute("UPDATE movies SET watched=watched+1 WHERE filename=?", (previous_video,))

    #debug
    #cur.execute("SELECT filename, watched FROM movies")
    #logger.debug("List of (filename, watched):    %s" % str(cur.fetchall()))

    db.commit()
    db.close()
    
"""
Name:       get_tags
Purpose:    Get list of tags for video with passed filename.
Parameter:  STRING representing video filename
Return:     LIST OF STRINGS representing tag names
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
Purpose:    Get a list of videos whose tags match all of those in the passed list
            (does not discriminate by watched attribute value)
Parameter:  LIST OF STRINGS representing tags
Return:     LIST OF STRINGS representing video filenames / NONE if no results
"""
def get_matching_videos(tag_list):
    db, cur = get_db_instance()

    #join tags in passed list into format for use in query below
    joined_tags = ' AND '.join(tag_list)

    #create virtual copy of movies table to allow use of MATCH in query
    fts_create_and_copy()
    
    #query for filename of video matching all passed tags
    cur.execute("SELECT filename FROM movies_fts WHERE tags MATCH ?", (joined_tags,))
    match_list = cur.fetchall()

    db.close()
    
    return match_list

"""
Name:       update_tags_favor
Purpose:    Update the value of each tag held by the video with passed filename.
            Change in value is based on passed values for attention and video review score.
Parameter:  STRING representing video filename, 
            FLOAT [0,1] representing failure or success to pay attention,
            INTEGER [1,5] representing user's video review score
Return:     none
"""
def update_tags_favor(filename, attention, score):
    db, cur = get_db_instance()
    
    #query and store list of tag names attributed to video with passed filename
    cur.execute("SELECT tags FROM movies WHERE filename=?", (filename,))
    tag_list = (cur.fetchone()[0]).split()

    #calculate change to tag favor based on user post-review score and attention modifier
    change_to_favor = (score - 3) / 2 + (attention - 3)

    logger.debug("Attention==%0.0f   Review==%d   Favor+=%0.1f" % (attention, score, change_to_favor))
    
    #initialize limits for the favor attribute
    max_favor = 39
    min_favor = 1

    #if change is positive, add to favor (to a maximum of 39) for all tags in list
    if change_to_favor > 0:
        for t in tag_list:
            cur.execute("UPDATE tags SET favor=MIN(favor+?, ?) WHERE name=?", (change_to_favor, max_favor, t))

    #if change is negative, subtract from favor (to a minimum of 1) for all tags in list
    elif change_to_favor < 0:
        for t in tag_list:
            cur.execute("UPDATE tags SET favor=MAX(favor+?, ?) WHERE name=?", (change_to_favor, min_favor, t))

    #debug
    #cur.execute("SELECT name,favor FROM tags")
    #logger.debug(cur.fetchall())

    db.commit()
    db.close()

"""
Name:       get_top_x_tags
Purpose:    Get a list of the top x tag names by their session priority (weight*favor) (larger number is stronger priority).
Parameter:  INTEGER representing number of tags names to get
Return:     LIST OF STRINGS representing tag names
"""
def get_top_x_tags(x):
    db, cur = get_db_instance()

    #query and store top x number of tags by descending priority
    cur.execute("SELECT name FROM tags ORDER BY weight*favor DESC LIMIT ?", (x,))
    temp = cur.fetchall()

    #initialize and fill list with tag names from above query
    tag_list = []
    for i in temp:
        tag_list.append(i[0])

    db.close()

    return tag_list

"""
Name:       get_next_ignore_tags
Purpose:    Return the filename of the video non-negative watched value. Tie goes to "lowest" filename
Parameter:  none
Return:     STRING representing video filename
"""
def get_next_ignore_tags():
    db, cur = get_db_instance()
    
    #query for video as described in function desc
    cur.execute("SELECT filename FROM movies WHERE watched>-1 ORDER BY watched ASC LIMIT 1")
    next_video = cur.fetchone()[0]
    
    db.close()

    return next_video

"""
Name:       get_best_match
Purpose:    Get filename of the video different from prev which has as many of the passed tags as possible and watched > -1.
            If there are multiple best matches by tag, the movie with lowest watched value is preferred.
Parameter:  STRING representing video filename,
            LIST OF STRINGS representing tag names
Return:     STRING representing video filename
"""
def get_best_match(previous_video, tag_list):
    db, cur = get_db_instance()
    
    #join tags in passed list into format for use in query below
    joined_tags = ' OR '.join(tag_list)
    
    #create virtual copy of movies table to facilitate use of MATCH keyword
    fts_create_and_copy()

    #query for video as described in this function's description comment
    logger.debug("Querying for tags: %s" % joined_tags)
    cur.execute("SELECT filename FROM movies_fts WHERE watched>-1 AND filename<>? AND tags MATCH ? ORDER BY bm25(movies_fts), watched", (previous_video, joined_tags,))
    temp = cur.fetchone()

    db.close()
    
    if temp is None:
        return None

    next_video = temp[0]
    return next_video

"""
Name:       update_prev_get_next
Purpose:    Essentially the driver function for previous video update and next video selection.
Parameter:  STRING representing video filename, 
            FLOAT [0,1] representing user's level of attention
            INTEGER [1,5] representing user's video review score
Return:     STRING representing video filename
"""
def update_prev_get_next(previous_video, attention, score):
    global num_tags
    
    #update watched value of previou video based on attention
    update_watched(previous_video, attention)

    #update favor for previous video's tags based on attention and score
    update_tags_favor(previous_video, attention, score)
    
    cu = count_unwatched()
    if cu == 0:
        return "No Video"
    elif cu == 1:
        return get_next_ignore_tags()

    x = 2 #set number of tags to use when querying best match video
    
    match = None #initialize variable for video filename
    
    while match is None:
        if (x > num_tags):
            return get_next_ignore_tags()
        tag_list = get_top_x_tags(x)
        match = get_best_match(previous_video, tag_list) #get filename for video which best matches those tags
        x += 1
        
    return match
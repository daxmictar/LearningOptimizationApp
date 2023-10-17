import sqlite3
from db_con import get_db
from tools.logging import logger

#drop and recreate movies table in local_data_base
def refresh_db():
    db = get_db()
    cur = db.cursor()

    #delete movies table
    cur.execute("DROP TABLE IF EXISTS movies")

    #create movies table 
    cur.execute("CREATE TABLE movies (filename TEXT NOT NULL, tags TEXT, watched INTEGER, priority INTEGER)")

    #insert rows descriptive of movies located in static
    cur.execute("INSERT INTO movies VALUES ('movie.mp4', 'Trees Bus Short', 0, 0)")
    cur.execute("INSERT INTO movies VALUES ('movie1.mp4', 'Beach Person Water Medium', 0, 0)")
    cur.execute("INSERT INTO movies VALUES ('movie2.mp4', 'Plants Bright Water Long', 0, 0)")
    cur.execute("INSERT INTO movies VALUES ('movie3.mp4', 'Trees Plants Long', 0, 0)")

    db.commit()

#in local_data_base, sets watched flag attribute of the video that has filename matching passed string
def set_watched(movie):
    db = get_db()
    cur = db.cursor()

    #if watched flag is not already set on video with passed string as filename...
    cur.execute("SELECT watched FROM movies WHERE filename=?", (movie,))
    if cur.fetchone()==(0,):
        #debug output
        logger.debug("Setting watched flag for " + movie)

        #set watched flag of video with passed string as name
        cur.execute("UPDATE movies SET watched=1 WHERE filename=?", (movie,))
        
    db.commit()

    #debug messages
    logger.debug("Unwatched videos:")
    cur.execute("SELECT filename FROM movies WHERE watched=0")
    logger.debug(cur.fetchall())
    logger.debug("Watched videos:")
    cur.execute("SELECT filename FROM movies WHERE watched=1")
    logger.debug(cur.fetchall())

#returns the filename of a random unwatched movie, or returns passed string (same video) if no unwatched videos remain
def get_unwatched(previous_video):
    db = get_db()
    cur = db.cursor()

    #if there are any more unwatched videos, randomly select one and return its filename
    cur.execute("SELECT COUNT(*) FROM movies WHERE watched=0")
    if cur.fetchone()[0]>0:
        # !!!ALERT!!! remember random() will be too expensive here when number of movies is large
        cur.execute("SELECT filename FROM movies WHERE watched=0 ORDER BY random()") 
        next_video = cur.fetchone()[0]

        logger.debug("Randomly selecting an unwatched video.")

        return next_video
    
    #else return the passed string (previous video filename)
    else:
        logger.debug("No unwatched videos remain. Replaying.")
        return previous_video
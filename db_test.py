import sqlite3
from flask import g
from db_con import get_db
from tools.logging import logger

#drop and recreate movie table in local_data_base
def refresh_db():
    db = get_db()
    cur = db.cursor()

    #delete movies table
    cur.execute("DROP TABLE IF EXISTS movies")

    #create movies table 
    cur.execute("CREATE TABLE movies (filename TEXT NOT NULL, tags TEXT, watched INTEGER, priority INTEGER)")

    #insert rows descriptive of movies located in static
    cur.execute("INSERT INTO movies VALUES ('movie.mp4', 'Trees Bus Short', 0, 0)")
    cur.execute("INSERT INTO movies VALUES ('movie2.mp4', 'Beach Person Water Medium', 0, 0)")
    cur.execute("INSERT INTO movies VALUES ('movie3.mp4', 'Plants Bright Water Long', 0, 0)")
    cur.execute("INSERT INTO movies VALUES ('movie4.mp4', 'Trees Plants Long', 0, 0)")

    db.commit()

#in local_data_base, set watched flag attribute of the movie that has filename matching passed string
def set_watched(movie):
    db = get_db()
    cur = db.cursor()

    #set watched flag of movie with passed string as name
    cur.execute("UPDATE movies SET watched=1 WHERE filename=?", (movie,))

    #debug output
    cur.execute("SELECT filename FROM movies WHERE watched=0")
    logger.debug(cur.fetchall())
    cur.execute("SELECT filename FROM movies WHERE watched=1")
    logger.debug(cur.fetchall())

    db.commit()
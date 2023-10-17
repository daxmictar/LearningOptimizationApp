import sqlite3
from flask import g
from db_con import get_db
from tools.logging import logger

#drop and recreate movie table in local_data_base
def refresh_db():
    db = get_db()
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS mov_unwatched;")
    cur.execute("DROP TABLE IF EXISTS mov_watched;")
    cur.execute("DROP TABLE IF EXISTS movies;")

    cur.execute("CREATE TABLE movies (id INTEGER PRIMARY KEY, filename TEXT NOT NULL, tags TEXT, watched INTEGER)")

    cur.execute("INSERT INTO movies VALUES (1, 'movie.mp4', 'Trees Bus Short', 0)")
    cur.execute("INSERT INTO movies VALUES (2, 'movie2.mp4', 'Beach Person Water Medium', 0)")
    cur.execute("INSERT INTO movies VALUES (3, 'movie3.mp4', 'Plants Bright Water Long', 0)")
    cur.execute("INSERT INTO movies VALUES (4, 'movie4.mp4', 'Trees Plants Long', 0);")

    db.commit()

def set_watched(movie):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE movies SET watched=1 WHERE filename=?", (movie,))
    cur.execute("SELECT filename FROM movies WHERE watched=0")
    logger.debug(cur.fetchall())
    cur.execute("SELECT filename FROM movies WHERE watched=1")
    logger.debug(cur.fetchall())
    db.commit()
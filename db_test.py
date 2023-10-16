import sqlite3
from flask import g

#drop and recreate tables in local_data_base
def refresh_db():
    g.cur.execute("DROP TABLE IF EXISTS mov_unwatched;")
    g.cur.execute("DROP TABLE IF EXISTS mov_watched;")
    g.cur.execute("CREATE TABLE mov_unwatched (id integer PRIMARY KEY, filename text NOT NULL, tags text)")
    g.cur.execute("CREATE TABLE mov_watched (id integer PRIMARY KEY, filename text NOT NULL, tags text)")
    
    g.cur.execute("INSERT INTO mov_unwatched VALUES (1, 'movie.mp4', 'Trees Bus Short')")
    g.cur.execute("INSERT INTO mov_unwatched VALUES (2, 'movie2.mp4', 'Beach Person Water Medium')")
    g.cur.execute("INSERT INTO mov_unwatched VALUES (3, 'movie3.mp4', 'Plants Bright Water Long')")
    g.cur.execute("INSERT INTO mov_unwatched VALUES (4, 'movie4.mp4', 'Trees Plants Long');")
    
    #g.cur.execute("SELECT * FROM ???;")
    #print(g.cur.fetchall())
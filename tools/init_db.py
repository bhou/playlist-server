import sqlite3
import os

import config

def create_table(conn, create_table_sql):
    """create database table"""
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

sql_create_video_table = """CREATE TABLE IF NOT EXISTS video (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    thumbnail TEXT NOT NULL
);"""

sql_create_playlist_table = """CREATE TABLE IF NOT EXISTS playlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    last_video_id INTEGER DEFAULT -1
);"""

sql_create_playlist_video_table = """CREATE TABLE IF NOT EXISTS playlist_video (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playlist_id INTEGER,
    video_id INTEGER,
    prev_video_id INTEGER DEFAULT -1
);"""


def init():
    """Initiate the data base, create the database table"""

    conn = sqlite3.connect(config.db_url)

    if conn is not None:
        # create video table
        create_table(conn, sql_create_video_table)

        # create playlist table
        create_table(conn, sql_create_playlist_table)

        # create playlist_video table
        create_table(conn, sql_create_playlist_video_table)

        conn.close()
    else:
        print("Error! failed to connect to database")

import sqlite3

import config

def create_playlist_op(cur, name, last_video_id = -1):
    """create a playlist"""

    sql = "INSERT INTO playlist (name, last_video_id) VALUES ('%s', %s)" % (name, last_video_id,)
    cur.execute(sql)
    return cur.lastrowid

def update_playlist_op(cur, id, name, last_video_id):
    """update the playlist"""

    sql = "UPDATE playlist SET name='%s', last_video_id=%s WHERE id=%s" % (name, last_video_id, id)
    cur.execute(sql)

def append_video_op(cur, playlist_id, new_video_id):
    """append a new video to playlist"""
    # get last playlist_video id
    sql = "SELECT last_video_id FROM playlist WHERE id=%s" % (playlist_id)
    cur.execute(sql)
    last_video_id = cur.fetchone()[0]


    # insert new playlist_video record
    sql = "INSERT INTO playlist_video (playlist_id, video_id, prev_video_id) VALUES (%s, %s, %s)" % (playlist_id, new_video_id, last_video_id)
    cur.execute(sql)
    new_playlist_video_id = cur.lastrowid

    # update playlist 
    sql = "UPDATE playlist SET last_video_id=%s WHERE id=%s" % (new_video_id, playlist_id,)
    cur.execute(sql)

    return new_playlist_video_id


def insert_video_op(cur, playlist_id, last_playlist_video_id, next_playlist_video_id, new_video_id):
    """insert a new video to playlist at the specific position (before next_playlist_video_id)"""

    if next_playlist_video_id >= 0:
        # insert
        # get next playlist_video record
        sql = "SELECT prev_playlist_video_id FROM playlist_video WHERE id=%s" % (next_playlist_video_id)
        cur.execute(cur)
        prev_playlist_video_id = cur.fetchone()[0]

        # insert new playlist_video record
        sql = "INSERT INTO playlist_video (playlist_id, video_id, prev_playlist_video_id) VALUES (%s, %s, %s)" % (playlist_id, new_video_id, prev_playlist_video_id)
        cur.execute(sql)
        new_playlist_video_id = cur.lasstrowid

        # update next playlist_video record
        sql = "UPDATE playlist_video SET prev_playlist_video=%s WHERE id=%s" % (new_playlist_video_id, next_playlist_video_id)
        cur.execute(sql)
    else:
        # append
        return append_video_op(cur, playlist_id, new_video_id)








def create_or_save(playlist):
    conn = sqlite3.connect(config.db_url)
    try:
        cur = conn.cursor()
        
        if playlist.id is None:
            # create video
            playlist.id = create_playlist_op(cur, playlist.name, playlist.last_video_id)
        else:
            # find the video
            cur.execute("SELECT * FROM playlist WHERE id=%s" % playlist.id)
            result = cur.fetchone()
            if result is None:
                playlist.id = create_playlist_op(cur, playlist.name, playlist.last_video_id)
            else:
                update_playlist_op(cur, playlist.id, playlist.name, playlist.last_video_id)

        conn.commit()
        conn.close()
    except conn.Error:
        conn.rollback()

def append_video(playlist, video):
    conn = sqlite3.connect(config.db_url)
    try:
        cur = conn.cursor()
        new_playlist_video_id = append_video_op(cur, playlist.id, video.id)

        conn.commit()
        conn.close()

        return new_playlist_video_id
    except conn.Error:
        conn.rollback()

def delete_playlist(playlist_id):
    conn = sqlite3.connect(config.db_url)
    
    cur = conn.cursor()
    
    # delete the playlist record
    sql = "DELETE FROM playlist WHERE id=%s" % (playlist_id,)
    cur.execute(sql)
    
    # delete the playlist video records
    sql = "DELETE FROM playlist_video WHERE playlist_id=%s" % (playlist_id,)
    cur.execute(sql)


    conn.commit()
    conn.close()

def delete_video(playlist, video_id):
    conn = sqlite3.connect(config.db_url)
    
    cur = conn.cursor()

    playlist_id = playlist.id
    
    # find the record of the to be deleted video
    sql = "SELECT * FROM playlist_video WHERE playlist_id=%s AND video_id=%s" % (playlist_id, video_id)
    cur.execute(sql)
    prev_video_id = cur.fetchone()[3]

    # find the next record of the to be delete video
    sql = "SELECT * FROM playlist_video WHERE playlist_id=%s AND prev_video_id=%s" % (playlist_id, video_id)
    cur.execute(sql)
    record = cur.fetchone()
    
    next_video_id = -1
    if record is None:
        next_video_id = -1
    else:
        next_video_id = record[2]

    # delete the record
    sql = "DELETE FROM playlist_video WHERE playlist_id=%s AND video_id=%s" % (playlist_id, video_id)
    cur.execute(sql)


    last_video_id = playlist.last_video_id
    # update link list
    if next_video_id >= 0:
        sql = "UPDATE playlist_video SET prev_video_id=%s WHERE playlist_id=%s AND video_id=%s" % (prev_video_id, playlist_id, next_video_id)
        cur.execute(sql)
    else:
        sql = "UPDATE playlist SET last_video_id=%s WHERE id=%s" % (prev_video_id, playlist_id)
        cur.execute(sql)
        last_video_id = prev_video_id

    conn.commit()
    conn.close()

    return last_video_id



def find_playlist_by_id(id):
    sql = "SELECT * FROM playlist WHERE id=%s" % (id,)
    
    conn = sqlite3.connect(config.db_url)
    
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    
    conn.commit()
    conn.close()

    return result

def find_all_playlists():
    sql = "SELECT * FROM playlist";
        
    conn = sqlite3.connect(config.db_url)
    
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
        
    conn.commit()
    conn.close()

    return result

def get_playlist_videos(playlist):
    # get all playlist video records
    conn = sqlite3.connect(config.db_url)
    
    cur = conn.cursor()
    sql = "SELECT * FROM playlist_video WHERE playlist_id=%s" % (playlist.id)
    cur.execute(sql)
    result = cur.fetchall()
    
    playlist_videos = {}
    video_ids = []
    for v in result:
        playlist_videos[("key-%s" % v[2])] = v
        video_ids.append(str(v[2]))

    # get all videos
    sql = "SELECT * FROM video WHERE id IN (%s)" % (",".join(video_ids))
    cur.execute(sql)
    result = cur.fetchall()

    videos = {}
    for v in result:
        videos[("key-%s" % v[0])] = v
    
    # order videos
    ret = []
    last_video_id = playlist.last_video_id
    while last_video_id >= 0:
        record = playlist_videos[("key-%s" % last_video_id)]
        
        ret.insert(0, videos[("key-%s" % record[2])])

        last_video_id = record[3]

    conn.commit()
    conn.close()

    return ret



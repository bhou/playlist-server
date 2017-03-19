import sqlite3

import config


def create_video_op(cur, title, thumbnail):
    sql = "INSERT INTO video (title, thumbnail) VALUES ('%s', '%s')" % (title, thumbnail,)
    cur.execute(sql)
    return cur.lastrowid

def update_video_op(cur, id, title, thumbnail):
    sql = "UPDATE video SET title='%s', thumbnail='%s' WHERE id=%s" % (title, thumbnail, id)
    cur.execute(sql)

def find_video_by_id_op(cur, id):
    sql = "SELECT * FROM video WHERE id=%s" % (id)
    cur.execute(sql)
    return cur.fetchone()




def create_or_save_video(video):
    conn = sqlite3.connect(config.db_url)
    try:
        cur = conn.cursor()
        
        if video.id is None:
            # create video
            video.id = create_video_op(cur, video.title, video.thumbnail)
        else:
            # find the video
            found = find_video_by_id_op(cur, video.id)
            if found is None:
                # the video with this id does not exist, just create a new video and assign a new id
                video.id = create_video_op(cur, video.title, video.thumbnail)
            else:
                update_video_op(cur, video.id, video.title, video.thumbnail)

        conn.commit()
        conn.close()
    except conn.Error:
        conn.rollback()

def find_video_by_id(id):
    conn = sqlite3.connect(config.db_url)
    
    cur = conn.cursor()
    result = find_video_by_id_op(cur, id)
    
    conn.commit()
    conn.close()

    return result

def find_all_videos():
    sql = "SELECT * FROM video"

    conn = sqlite3.connect(config.db_url)
    
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()

    conn.commit()
    conn.close()

    return result


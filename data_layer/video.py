import json

from data_source.sqlite.video import create_or_save_video, find_video_by_id, find_all_videos

class Video:
    """Video class represents a video record"""

    def __init__(self, id, title, thumbnail):
        self.id = id
        self.title = title
        self.thumbnail = thumbnail

    def save(self):
        create_or_save_video(self)

    def toJSONSerializable(self):
        return {
                'id': self.id,
                'title': self.title,
                'thumbnail': self.thumbnail
            }
        
    @staticmethod
    def createVideo(title, thumbnail):
        return Video(None, title, thumbnail)

    @staticmethod
    def findVideoById(id):
        result = find_video_by_id(id)
        
        ret = None
        if result is None:
            ret = None
        else:
            ret = Video(result[0], result[1], result[2])
        
        return ret

    @staticmethod
    def findAll():
        result = find_all_videos()
        ret = map(lambda v: Video(v[0], v[1], v[2]), result)
        return ret



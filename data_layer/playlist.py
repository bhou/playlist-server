from data_source.sqlite.playlist import (
        create_or_save, 
        append_video, 
        find_playlist_by_id, 
        find_all_playlists, 
        delete_playlist,
        get_playlist_videos,
        delete_video)

from data_layer.video import Video


class PlayList:
    """PlayList class represents a video playlist"""

    def __init__(self, id, name, last_video_id):
        self.id = id
        self.name = name
        self.last_video_id = last_video_id

    def save(self):
        create_or_save(self)

    def delete(self):
        delete_playlist(self.id)
        
    def addVideo(self, video):
        append_video(self, video)
        self.last_video_id = video.id


    def getVideos(self):
        result = get_playlist_videos(self)
        return map(lambda v: Video(v[0], v[1], v[2]), result)

    def deleteVideo(self, video_id):
        self.last_video_id = delete_video(self, video_id)

    def toJSONSerializable(self):
        return {
                    'id': self.id,
                    'name': self.name,
                    'last_video_id': self.last_video_id
                }

    @staticmethod
    def createPlaylist(name, last_video_id = -1):
        return PlayList(None, name, last_video_id)

    @staticmethod
    def findPlaylistById(id):
        result = find_playlist_by_id(id)
        
        ret = None
        if result is None:
            ret = None
        else:
            ret = PlayList(result[0], result[1], result[2])
        
        return ret
    
    @staticmethod
    def findAll():
        result = find_all_playlists()

        ret = map(lambda v: PlayList(v[0], v[1], v[2]), result)

        return ret





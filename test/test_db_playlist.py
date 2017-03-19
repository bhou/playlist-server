import unittest

from data_layer.playlist import PlayList
from data_layer.video import Video

class TestPlaylistDB(unittest.TestCase):

    def test_create_and_find_playlist(self):
        playlist = PlayList.createPlaylist('playlist for test')
        playlist.save()
        
        id = playlist.id
        # find the video
        newPlaylist = PlayList.findPlaylistById(id)
        
        self.assertFalse(id is None)
        self.assertEqual(newPlaylist.id, playlist.id)

    def test_modify_playlist(self):
        playlist = PlayList.createPlaylist('playlist for test')
        playlist.save()

        self.assertFalse(playlist.id is None)
        self.assertEqual(playlist.name, 'playlist for test')
        self.assertEqual(playlist.last_video_id, -1)

        playlist.name = 'modified playlist for test'
        playlist.last_video_id = 2

        playlist.save()

        self.assertEqual(playlist.name, 'modified playlist for test')
        self.assertEqual(playlist.last_video_id, 2)

        newPlaylist = PlayList.findPlaylistById(playlist.id)
        self.assertEqual(newPlaylist.name,  'modified playlist for test')
        self.assertEqual(newPlaylist.last_video_id, 2)

    def test_append_video(self):
        playlist = PlayList.createPlaylist('playlist for test')
        playlist.save()

        video1 = Video.createVideo('video 1', 'http://localhost:9080/video/1234')
        video1.save()

        video2 = Video.createVideo('video 1', 'http://localhost:9080/video/1234')
        video2.save()

        video3 = Video.createVideo('video 1', 'http://localhost:9080/video/1234')
        video3.save()

        playlist.addVideo(video1)
        playlist.addVideo(video2)
        playlist.addVideo(video3)

        playlistVideos = playlist.getVideos()


        self.assertEqual(playlistVideos[0].id, video1.id)
        self.assertEqual(playlistVideos[1].id, video2.id)
        self.assertEqual(playlistVideos[2].id, video3.id)

    def test_delete_video(self):
        playlist = PlayList.createPlaylist('playlist for test')
        playlist.save()

        video1 = Video.createVideo('video 1', 'http://localhost:9080/video/1234')
        video1.save()

        video2 = Video.createVideo('video 1', 'http://localhost:9080/video/1234')
        video2.save()

        video3 = Video.createVideo('video 1', 'http://localhost:9080/video/1234')
        video3.save()

        playlist.addVideo(video1)
        playlist.addVideo(video2)
        playlist.addVideo(video3)

        playlist.deleteVideo(video2.id)

        playlistVideos = playlist.getVideos()

        self.assertEqual(len(playlistVideos), 2)
        self.assertEqual(playlistVideos[0].id, video1.id)
        self.assertEqual(playlistVideos[1].id, video3.id)

    def test_delete_last_video(self):
        playlist = PlayList.createPlaylist('playlist for test')
        playlist.save()

        video1 = Video.createVideo('video 1', 'http://localhost:9080/video/1234')
        video1.save()

        video2 = Video.createVideo('video 1', 'http://localhost:9080/video/1234')
        video2.save()

        video3 = Video.createVideo('video 1', 'http://localhost:9080/video/1234')
        video3.save()

        playlist.addVideo(video1)
        playlist.addVideo(video2)
        playlist.addVideo(video3)

        playlist.deleteVideo(video3.id)

        playlistVideos = playlist.getVideos()

        self.assertEqual(len(playlistVideos), 2)
        self.assertEqual(playlistVideos[0].id, video1.id)
        self.assertEqual(playlistVideos[1].id, video2.id)



    def test_delete_playlist(self):
        playlist = PlayList.createPlaylist('playlist for test')
        playlist.save()

        self.assertFalse(playlist.id is None)
        self.assertEqual(playlist.name, 'playlist for test')
        self.assertEqual(playlist.last_video_id, -1)

        playlist.delete()

        newPlaylist = PlayList.findPlaylistById(playlist.id)
        self.assertIsNone(newPlaylist)



if __name__ == '__main__':
    unittest.main()

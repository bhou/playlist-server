import unittest

from data_layer.video import Video

class TestVideoDB(unittest.TestCase):

    def test_create_and_find_video(self):
        video = Video.createVideo('video for test', 'http://localhost:9080/video/1234')
        video.save()
        
        id = video.id
        # find the video
        newVideo = Video.findVideoById(id)
        
        self.assertFalse(id is None)
        self.assertEqual(newVideo.id, video.id)

    def test_modify_video(self):
        video = Video.createVideo('video for test', 'http://localhost:9080/video/1234')
        video.save()
        
        self.assertFalse(video.id is None)
        self.assertEqual(video.title, 'video for test')

        video.title = 'modified video title for test'

        video.save()
        self.assertEqual(video.title, 'modified video title for test')

        newVideo = Video.findVideoById(video.id)
        self.assertEqual(newVideo.title,  'modified video title for test')



if __name__ == '__main__':
    unittest.main()

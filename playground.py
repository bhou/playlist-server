import config

from data_layer.video import Video
from data_layer.playlist import PlayList

from data_source.video import create_video_op

print create_video_op

video = Video.findVideoById(1)
print video.id, ';', video.title, ';', video.thumbnail

Video.findAll()

"""
video1 = Video.createVideo('this is a title', 'http://localhost:9080/video/1234')

print video1.id

video1.save()

print video1.id

video1.title = 'Modified title'

video1.save()

print video1.id
print video1.title
"""


"""
playlist1 = PlayList.createPlayList('this is a playlist')

print playlist1.id

playlist1.save()

print playlist1.id
"""

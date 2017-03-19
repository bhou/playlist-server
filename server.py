import json

import jwt

import config

from bottle import route, run, template, request, response, HTTPError 

from data_layer.video import Video
from data_layer.playlist import PlayList

from data_layer.data_exception import DataLayerException

#def protected(verify):
def protected():
    def verify_token(func):
        def wrapper(*a, **ka):
            header = request.get_header('Authorization')
            if header is None:
                response.headers['Content-Type'] = 'application/json'
                response.status = 401
                return json.dumps({'error':'Unauthorized'})
            
            try:
                encoded = header[7:]

                # TODO: verify the token here
                # token = jwt.decode(encoded, config.jwt_secret, algorithms=['HS256'])
                # verify(token)

            except:
                response.headers['Content-Type'] = 'application/json'
                response.status = 401
                return json.dumps({'error':'Unauthorized'})


            return func(*a, **ka)
        return wrapper
    return verify_token


@route('/videos/<name>')
@protected()
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/videos', method=['GET'])
@protected()
def get_all_videos():
    try:
    
        videos = Video.findAll()
    
    except DataLayerException:
        response.status = e.errorArgs['code']
        return json.dumps({'error': e.errorArgs['message']})

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': map(lambda v: v.toJSONSerializable(), videos)})


@route('/video', method=['POST'])
@protected()
def create_video():
    """create a new video, it accept an json object as the body:
    {
        "title": "the title of the video",
        "thumbnail": "the url of the video"
    }
    """
    try:
        try:
            data = request.json
        except:
            raise ValueError
        
        if data is None:
            raise ValueError
        
        if data['title'] is None:
            raise ValueError

        if data['thumbnail'] is None:
            raise ValueError
        
        video = Video.createVideo(data['title'], data['thumbnail'])

        video.save()

    except ValueError as e:
        response.status = 400
        return json.dumps({'error': 'Bad Request'})

    except DataLayerException as e:
        response.status = e.errorArgs['code']
        return json.dumps({'error': e.errorArgs['message']})

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': video.toJSONSerializable()})

    





@route('/playlists', method=['GET'])
@protected()
def get_all_playlists():
    try:
    
        playlists = PlayList.findAll()
    
    except DataLayerException:
        response.status = e.errorArgs['code']
        return json.dumps({'error': e.errorArgs['message']})


    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': map(lambda v: v.toJSONSerializable(), playlists)})

@route('/playlist/<id>/videos', method=['GET'])
@protected()
def get_playlist_videos(id):
    try:
    
        playlist = PlayList.findPlaylistById(id)

        if playlist is None:
            raise DataLayerException({'code' :404, 'message': 'No play list found'})

        videos = playlist.getVideos();
    
    except DataLayerException as e:
        response.status = e.errorArgs['code']
        return json.dumps({'error': e.errorArgs['message']})
    
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': map(lambda v: v.toJSONSerializable(), videos)})

@route('/playlist/<id>', method=['GET'])
@protected()
def get_playlist_info(id):
    try:
    
        playlist = PlayList.findPlaylistById(id)

        if playlist is None:
            raise DataLayerException({'code' :404, 'message': 'No play list found'})

    except DataLayerException as e:
        response.status = e.errorArgs['code']
        return json.dumps({'error': e.errorArgs['message']})

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': playlist.toJSONSerializable()})


@route('/playlist', method=['POST'])
@protected()
def create_playlist():
    """create a new playlist, it accept an json object as the body:
    {
        "name": "the new playlist name"
    }
    """
    try:
        try:
            data = request.json
        except:
            raise ValueError
        
        if data is None:
            raise ValueError
        
        if data['name'] is None:
            raise ValueError
        
        playlist = PlayList.createPlaylist(data['name'])

        if playlist is None:
            raise DataLayerException({'code' :404, 'message': 'No play list found'})

        playlist.name = data['name']

        playlist.save()

    except ValueError as e:
        response.status = 400
        return json.dumps({'error': 'Bad Request'})

    except DataLayerException as e:
        response.status = e.errorArgs['code']
        return json.dumps({'error': e.errorArgs['message']})

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': playlist.toJSONSerializable()})

@route('/playlist/<id>', method=['PUT'])
@protected()
def update_playlist(id):
    """update a playlist, it accept an json object as the body:
    {
        "name": "the new playlist name"
    }
    """
    try:
        try:
            data = request.json
        except:
            raise ValueError
        
        if data is None:
            raise ValueError
        
        if data['name'] is None:
            raise ValueError
        
        playlist = PlayList.findPlaylistById(id)

        if playlist is None:
            raise DataLayerException({'code' :404, 'message': 'No play list found'})
        
        playlist.name = data['name']

        playlist.save()

    except ValueError as e:
        response.status = 400
        return json.dumps({'error': 'Bad Request'})

    except DataLayerException as e:
        response.status = e.errorArgs['code']
        return json.dumps({'error': e.errorArgs['message']})

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': playlist.toJSONSerializable()})

@route('/playlist/<id>', method=['DELETE'])
@protected()
def delete_playlist(id):
    try:
        playlist = PlayList.findPlaylistById(id)

        if playlist is None:
            raise DataLayerException({'code' :404, 'message': 'No play list found'})
        
        playlist.delete()

    except ValueError as e:
        response.status = 400
        return json.dumps({'error': 'Bad Request'})

    except DataLayerException as e:
        response.status = e.errorArgs['code']
        return json.dumps({'error': e.errorArgs['message']})

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': 'OK'})


@route('/playlist/<playlist_id>/<video_id>', method=['PUT'])
@protected()
def add_video_to_playlist(playlist_id, video_id):
    try:
        playlist = PlayList.findPlaylistById(playlist_id)

        if playlist is None:
            raise DataLayerException({'code' :404, 'message': 'No play list found'})
        
        video = Video.findVideoById(video_id)

        if video is None:
            raise DataLayerException({'code' :404, 'message': 'No video found'})

        playlist.addVideo(video)

    except ValueError as e:
        response.status = 400
        return json.dumps({'error': 'Bad Request'})

    except DataLayerException as e:
        response.status = e.errorArgs['code']
        return json.dumps({'error': e.errorArgs['message']})

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': 'OK'})

@route('/playlist/<playlist_id>/<video_id>', method=['DELETE'])
@protected()
def delete_video_from_playlist(playlist_id, video_id):
    try:
        playlist = PlayList.findPlaylistById(playlist_id)

        if playlist is None:
            raise DataLayerException({'code' :404, 'message': 'No play list found'})
        
        playlist.deleteVideo(video_id)

    except ValueError as e:
        response.status = 400
        return json.dumps({'error': 'Bad Request'})

    except DataLayerException as e:
        response.status = e.errorArgs['code']
        return json.dumps({'error': e.errorArgs['message']})

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': 'OK'})


run(host='localhost', port=8080)

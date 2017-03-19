# playlist-server

[![Build Status](https://travis-ci.org/bhou/playlist-server.svg?branch=master)](https://travis-ci.org/bhou/playlist-server)

# Architecture

Three Layers:

- Web Access layer: handles web request (input validation, authentication, authorization, etc)
- Business layer: provides business related data access API
- Data connector layer: provides raw data access API, this layer is data-source-aware, we can implement this layer with different data sources and different data source libraries/drivers.

`````text
--------------------------------------
|                 web api            |
--------------------------------------
|              business layer        |
--------------------------------------
|  mysql connector | mongo connector |  
--------------------------------------
`````

# Data Structure and Time Complexity Considerations

Two entities: video and playlist 

A video can be put into mutiple playlists, and a playlists contains multiple videos. This is a typical many to many relationship. To represent such relationship in relational database like mysql, we need three tables:

- video table: each row in this table represents a video
- playlist table: each row in this table represents a playlist
- playlist_video table: each row in this table represents a video in a playlist

The operation requires that the video order in playlist is persisted when a video is added, deleted, and moved (change order), one possible solution is to keep an order column in the **playlist_video** table, and update the order when a video is added/deleted/moved. With such a data structure, for a playlist with **N** video, the time complexity is **O(N)** (for delete and move).

To reduce the time complexity of the playlist operations, a linked list is used in the data base table design:

- each record in *playlist_video* table has a **prev_video_id** column to record the previous video
- in *playlist* table, a column named **last_video_id** is used to record the last video in playlist

With this data structure, all operations (added/deleted/moved) have a time complexity of **O(1)** (constant time).


**video** Table

| id  | title | thumbnail |
| ------------- | ------------- | --------------|
| integer, video id | string, video title  | string, the url of the video |


**playlist** Table

| id  | name | last_video_id |
| ------------- | ------------- | --------------|
| integer, playlist id | string, the playlist name | integer, the id of the last video in the playlist |

**playlist_video** Table

Each record in this table represents a video in playlist

| id  | playlist_id | video_id | prev_video_id |
| ------------- | ------------- | --------------|----------------|
| integer, unique id | integer, the playlist id | integer, the id video id | integer, the id of the previous video |

# Rest API

## Response Format Convention

Response data is in json format: 

**success**

With status code 200
`````json
{
  "data": "could be an object, an array or a string"
}
`````

**fail**

With failed status code
`````json
{
  "error": "error message"
}
`````

## API

#### GET /videos

Get all videos



#### POST /video

Create video

###### Request:

`````json
{
  "title": "video name",
  "thumbnail": "video url"
}
`````
###### Response:

`````javascript
{
  "data": {} // the created video object
}
`````


#### GET /playlists

Get all playlists

###### Response:

`````javascript
{
  "data": [] // the list of playlist
}
`````

#### GET /playlist/:id

Get playlist information

- id: the id of the playlist

###### Response:

`````javascript
{
  "data": {} // the playlist information
}
`````


#### GET /playlist/:id/videos

Get all videos in playlist

- id: the id of the playlist

###### Response:

`````javascript
{
  "data": [] // the list of video in playlist
}
`````


#### POST /playlist

Create playlist

###### Request:

`````json
{
  "name": "playlist name",
}
`````
###### Response:

`````javascript
{
  "data": {} // the created playlist object
}
`````


#### PUT /playlist/:id

Modify the playlist information

- id: the playlist id

###### Request:

`````json
{
  "name": "new playlist name",
}
`````
###### Response:

`````javascript
{
  "data": {} // the modified playlist object
}
`````


#### DELETE /playlist/:id

Delete the playlist (it will delete the playlist record in *playlist* table, and all the records related to it in *playlist_video* )

- id: the playlist id

###### Request:

`````json
{
  "name": "new playlist name",
}
`````
###### Response:

`````javascript
{
  "data": "OK"
}
`````



#### PUT /playlist/:playlist_id/:video_id

Add a video in playlist

- playlist_id: the playlist id
- video_id: the video id

###### Response:

`````javascript
{
  "data": "OK"
}
`````



#### DELETE /playlist/:playlist_id/:video_id

Delete a video from playlist

- playlist_id: the playlist id
- video_id: the video id

###### Response:

`````javascript
{
  "data": "OK"
}
`````

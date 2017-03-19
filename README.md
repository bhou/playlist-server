# playlist-server

[![Build Status](https://travis-ci.org/bhou/playlist-server.svg?branch=master)](https://travis-ci.org/bhou/playlist-server)

# How to run it

First, initiate the data base

```sh
python create_db_table.py
```

Run the server

```sh
python server.py
```

# Unit Tests

Build and test status see [https://travis-ci.org/bhou/playlist-server](https://travis-ci.org/bhou/playlist-server)

```sh
python -m unittest discover
```

# Architecture

Three Layers:

- Web Access layer: handles web request (input validation, authentication, authorization, etc)
- Business layer: provides business related data access API
- Data connector layer: provides raw data access API, this layer is data-source-aware, we can implement this layer with different data sources and different data source libraries/drivers.

The idea here is to isolate the underlying database implemenation details and provides a business friendly Data access API.

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

The operation requires that the video order in playlist is persisted when a video is added, deleted, and moved (change order), one possible solution is to keep an order column in the **playlist_video** table, and update the order when a video is added/deleted/moved. With such a data structure, for a playlist with **N** video, the time complexity is **O(N)** (worst case for delete and move).

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

## Security

The server is not protected by HTTPS. 

NOTICE: Always deploy it behind a reverse proxy with HTTPS enabled. You can benefits not only the security but also load balancing, 0 down time deployment, etc. 

## Authentication/Authorization

APIs are protected by token based authentication/authorization system. The distribution of token is not included in this server, please use a Oauth2 or SAML federation server to distribute the token and use the token in all your API requests:

> Authorization: Bearer [your token]

In *server.py*, modify the `protected` function to verify the token (Now the verification is disabled for demo)

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

## Other considerations

The current implementation uses a relational database to store the data model. It is possible to use a non-sql database to store the data and gain performance boost understand the following consideration:

1. video information is small (only contains title and url)
2. playlist length usually is small (for a video playlist case, 200 videos in a playlist is already a big and rare video list)

We can store such playlist in a single json document as following: (for example, mongo DB single document limit is 16M)
```js
playlist = {
  name: 'playlist name',
  videos: [
    {
      id: 'video 1 id',
      title: 'video 1 title',
      thumbnail: 'video 1 url'
    },
    {
      id: 'video 2 id',
      title: 'video 2 title',
      thumbnail: 'video 2 url'
    },
    ...
  ]
}
```

A single db query can get the whole playlist 

#### Drawbacks with this non-sql implementation:

Data inconsistent when original video information is changed. Need to update all video sub documents in all playlists.

A possible solution to this problem could be storing a list of video id in the playlist document, and make a second db query to get the video informations.

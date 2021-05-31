# Obtain Lyrics with [Genius API](https://docs.genius.com/)

This service is connected with ['Manager'](https://github.com/mer-team/Tests/blob/rabbit-manager/Manager/manager.js) service through [RabbitMQ](https://www.rabbitmq.com/). Checks whether it is possible to obtain the lyric of a song and, if possible, save that lyric in a text file.

Run `python3.7 genius.py`

## Input through RabbitMQ
```javascript
{ "song": "Track Name", "artist": "Artist Name", "vID": "videoid" }
                     OR                      
{ "song": "Undefined"," artist": "Undefined" }
```
Example:
```javascript
{ "song": "happier", "artist": "marshmello", "vID": "m7Bc3pLyij0" }
```

## Output
```javascript
{ "Service": "LyricsExtractor", "Result": { "Filename": "SongName.txt" } }
                                 OR                                  
{ "Service": "LyricsExtractor", "Result": { "Filename": "Music Not Found" } }
```

## Docker Params
| Arg | Default | Description |
| --- | --- | --- |
| HOST | localhost | RabbitMQ host |
| USER | guest | HTTP basic auth username  |
| PASS | guest | HTTP basic auth password |
| PORT | 5672 | RabbitMQ Port |
| MNG_PORT | 15672 | RabbitMQ Management Port |
| TIME | 10 | Timeout to check if the service is up |
| GENIUS_KEY | apikey | Genius API key |

## Run Local Microservice
Run Rabbit
```
docker run -d -e RABBITMQ_DEFAULT_USER=merUser -e RABBITMQ_DEFAULT_PASS=passwordMER -p 15672:15672 -p 5672:5672 rabbitmq:3-management-alpine
```

Build local `LyricsExtractor` from source
```
docker build -t lyricsextractor:local .
```

Run local `LyricsExtractor`
```
docker run -e TIME=10 -e USER=merUser -e PASS=passwordMER -e HOST=localhost -e PORT=5672 -e MNG_PORT=15672 -e LAST_FM_KEY=apikey --net=host -v "<Local DIR>:/Audios" lyricsextractor:local
```

Run official `LyricsExtractor` image locally
```
docker run -e TIME=10 -e USER=merUser -e PASS=passwordMER -e HOST=localhost -e PORT=5672 -e MNG_PORT=15672 -e LAST_FM_KEY=apikey --net=host -v "<Local DIR>:/Audios" merteam/lyricsextractor:latest
```

## Tests
The tests can be accessed on the `test` folder. Test list:
- [x] Check the RabbitMQ connection
- [x] Create a RabbitMQ channel
- [x] Send a music to find the lyrics
- [x] Check if the file with the lyrics exists
- [ ] Check the hash of the received file 
- [ ] Check the RabbitMQ response and compare it to the expected one (commented, only works locally)
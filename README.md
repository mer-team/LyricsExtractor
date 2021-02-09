# Obtain Lyrics with [Genius API](https://docs.genius.com/)

This service is connected with ['Manager'](https://github.com/mer-team/Tests/blob/rabbit-manager/Manager/manager.js) service through [RabbitMQ](https://www.rabbitmq.com/). Checks whether it is possible to obtain the lyric of a song and, if possible, save that lyric in a text file.

Run `python3.7 genius.py`

## Input through RabbitMQ

```javascript
{ song: 'Track Name', artist: 'Artist Name' }
                     OR                      
{ song: 'Undefined', artist: 'Undefined' }
```

## Output

```javascript
{ Service: "LyricsExtractor", Result: { Filename: 'SongName.txt' } }
                                 OR                                  
{ Service: "LyricsExtractor", Result: { Filename: 'Music Not Found' } }
```
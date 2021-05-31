# https://lyricsgenius.readthedocs.io/en/master/
import lyricsgenius as lg
from pathlib import Path
import os
import pika
import json

from dotenv import load_dotenv
load_dotenv()

mqhost = os.environ.get("HOST")
mquser = os.environ.get("USER")
mqpass = os.environ.get("PASS")
mqport = os.environ.get("PORT")
API_KEY=os.environ.get("GENIUS_KEY")

credentials =  pika.PlainCredentials(mquser, mqpass)
connection = pika.BlockingConnection(pika.ConnectionParameters(mqhost, mqport,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='lyrics')

genius = lg.Genius(API_KEY,
                    skip_non_songs=True,
                    remove_section_headers=True,
                    excluded_terms = ["(Remix)", "(Live)"],
                    verbose = False)

def callback(ch, method, properties, body):
    info = json.loads(body.decode('utf-8'))
    print(" [x] Received %r" % info)
    if "song" in info and "artist" in info:
        song = genius.search_song(info['song'], info['artist'])
    else:
        song = None

    if song != None:
        s = song.save_lyrics(filename=info['vID'], extension='txt', overwrite='true')
        filename = info['vID'] + ".txt"

        # create path if doesn't exist
        Path("/Audios/" + info['vID']).mkdir(parents=True, exist_ok=True)
        # sets the filename to the vID and save it to the vID dir
        os.rename("./" + filename, "/Audios/" + info['vID'] + "/" + filename)

        msg = {
            "Service": "LyricsExtractor",
            "Result": { "vID": info['vID'], "Filename": filename }
        }

        channel.basic_publish(exchange='',
                        routing_key='management',
                        body=json.dumps(msg))
        print(" [x] Sent %s to management" % msg)
    else:
        msg = {
            "Service": "LyricsExtractor",
            "Result": { "vID": info['vID'], "Filename": "Music Not Found" }
        }
        channel.basic_publish(exchange='',
                        routing_key='management',
                        body=json.dumps(msg))
        print(" [x] Sent %s to management" % msg)

channel.basic_consume(queue='lyrics',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
# https://lyricsgenius.readthedocs.io/en/master/
import lyricsgenius as lg
import os
import pika
import json

from dotenv import load_dotenv
load_dotenv()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='lyrics')

API_KEY=os.environ.get("GENIUS_KEY")

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
        s = song.save_lyrics(filename=info['song'], extension='txt', overwrite='true')
        filename = info['song'] + ".txt"
        msg = {
            "Service": "LyricsExtractor",
            "Result": { "Filename": filename }
        }

        channel.basic_publish(exchange='',
                        routing_key='management',
                        body=json.dumps(msg))
        print(" [x] Sent %s to management" % msg)
    else:
        msg = {
            "Service": "LyricsExtractor",
            "Result": { "Filename": "Music Not Found" }
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
FROM python:3.7-slim

ARG HOST=localhost
ARG USER=merUser
ARG PASS=passwordMER
ARG PORT=5672
ARG MNG_PORT=15672
ARG TIME=10
ARG GENIUS_KEY=apikey

COPY /src /lyricsExtractor

WORKDIR /lyricsExtractor

RUN apt-get update && apt-get install curl -y && \
    rm -rf /var/lib/apt/lists && mkdir /Audios && \
    pip install -r ./requirements.txt && \
    chmod +x ./wait-for-rabbit.sh

CMD ["./wait-for-rabbit.sh", "python", "genius.py"]
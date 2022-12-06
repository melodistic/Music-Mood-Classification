FROM ubuntu:18.04 as downloader

ENV DEBIAN_FRONTEND=noninteractive

RUN apt -y update
RUN apt install -y python3.8 && update-alternatives --install /usr/bin/python python /usr/bin/python3.8 10
RUN apt install -y python3-pip
RUN python -m pip install --upgrade pip
RUN apt install -y ffmpeg
RUN apt install -y git

RUN mkdir /app

WORKDIR /app

COPY download_requirements.txt .

RUN pip install -r download_requirements.txt

COPY download_video.py .
COPY song_list.csv .

RUN python download_video.py

FROM tensorflow/tensorflow:2.8.0

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

RUN apt-get install -y libpq-dev python-dev

RUN apt-get install -y git

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install git+https://github.com/GGolfz/spleeter.git@master#egg=spleeter

RUN mkdir /app/song
COPY --from=downloader /app/song /app/song

COPY extract_song.py .

RUN python extract_song.py

COPY generate_spectrogram.py .

RUN python generate_spectrogram.py

COPY process_data.py .
COPY model_v1.h5 .

RUN mkdir /app/features
RUN mkdir /app/csv_data

RUN python process_data.py

COPY combine_csv.py .

RUN python combine_csv.py

COPY generate_csv_feature.py .

RUN python generate_csv_feature.py
FROM --platform=linux/x86_64 python:3.9

ENV TZ="Asia/Tokyo"
RUN echo $TZ > /etc/timezone

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get install -y iputils-ping net-tools libgl1-mesa-dev\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y gstreamer1.0-tools gstreamer1.0-nice gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
    gstreamer1.0-plugins-good gstreamer1.0-rtsp gstreamer1.0-alsa gstreamer1.0-libav --fix-missing \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y network-manager network-manager-gnome \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

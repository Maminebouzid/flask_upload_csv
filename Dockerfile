FROM python:3.9

RUN apt-get update && apt-get -y install git wget build-essential
RUN apt install -y libsm6 libxext6 libgl1-mesa-glx libopengl0 libegl1 libxkbcommon-x11-0 #pytest libraries


RUN pip3 install --upgrade pip

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt
EXPOSE 8080:8080

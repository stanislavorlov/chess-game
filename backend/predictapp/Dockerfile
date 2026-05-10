FROM python:3.13.2-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /predictapp

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

COPY predictapp/requirements.txt /predictapp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY predictapp/ /predictapp/predictapp/
COPY chessengine/ /predictapp/chessengine/
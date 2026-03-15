FROM python:3.13.2-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /chessapp

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

COPY chessapp/requirements.txt /chessapp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY chessapp/ /chessapp/chessapp/
COPY chessengine/ /chessapp/chessengine/
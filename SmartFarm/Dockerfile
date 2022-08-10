# syntax=docker/dockerfile:1
FROM python:3.8-slim

WORKDIR /code

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP=App

COPY . .
RUN apt update && apt upgrade -y
RUN pip install -r installs/requirements.txt

EXPOSE 5000

# RUN flask init-db

CMD ["flask", "run"]
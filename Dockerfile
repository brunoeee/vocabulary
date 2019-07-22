FROM python:3.7-alpine3.10

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev 

COPY . /app
WORKDIR /app

RUN ["pip", "install", "-r", "requirements.txt"]
RUN ["chmod", "+x", "wait-for"]
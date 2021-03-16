FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV STATIC_PATH /app/app/static

RUN apt update

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

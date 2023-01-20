FROM python:3.8-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uwsgi","uwsgi.ini"]
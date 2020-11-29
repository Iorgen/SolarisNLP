# pull official base image
FROM python:3.6

RUN mkdir -p /usr/src/face_recog_api/
COPY ./requirements.txt /usr/src/face_recog_api

# set work directory
WORKDIR /usr/src/face_recog_api

# Update pip and from requirements.txt install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install keybert

ENV BUILD_VERSION=debug

COPY ./ .

# prepare wait-for-command.sh
COPY wait-for-command.sh /usr/bin/wait-for-command
RUN chmod +x /usr/bin/wait-for-command

# RUN chmod +x boot.sh
CMD PYTHONPATH=. alembic upgrade head ; \
    gunicorn -c gunicorn.conf.py wsgi

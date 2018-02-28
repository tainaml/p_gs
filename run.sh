#!/bin/bash

NAME="rede_gsti"
DJANGODIR=/var/www/rede_gsti
SOCKFILE=/var/www/rede_gsti/run/gunicorn.sock
USER=ubuntu
GROUP=www-data
NUM_WORKERS=9
DJANGO_SETTINGS_MODULE=rede_gsti.settings
DJANGO_WSGI_MODULE=rede_gsti.wsgi
PROJECT_ENVIRONMENT=production
IP_PORT_PAIR=127.0.0.1:8000

echo "Starting $NAME as `whoami`"


cd $DJANGODIR
source $DJANGODIR/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export PROJECT_ENVIRONMENT=$PROJECT_ENVIRONMENT
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR


exec venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  -b $IP_PORT_PAIR \
  --workers $NUM_WORKERS \
  --user=$USER \
  --bind=unix:$SOCKFILE
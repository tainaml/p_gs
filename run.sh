#!/bin/bash

NAME="PORTAL GSTI"
DJANGODIR=/var/www/rede_gsti
SOCKFILE=/var/www/rede_gsti/run/gunicorn.sock
USER=ubuntu
GROUP=www-data
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=rede_gsti.settings
DJANGO_WSGI_MODULE=rede_gsti.wsgi
PROJECT_ENVIRONMENT=production

echo "Starting $NAME as `whoami`"


cd $DJANGODIR
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export PROJECT_ENVIRONMENT=$PROJECT_ENVIRONMENT

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR


exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE
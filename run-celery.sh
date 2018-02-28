#!/bin/bash

DJANGO_DIR=/var/www/rede_gsti
PROJECT=rede_gsti
LOG_LEVEL=info

cd $DJANGO_DIR
export PROJECT_ENVIRONMENT=production
source $DJANGO_DIR/venv/bin/activate
celery -A $PROJECT worker -l $LOG_LEVEL
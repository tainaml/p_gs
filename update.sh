#!/bin/bash

# Declaring LOG and Branch vars
LOG_PATH="/var/log/rede_gsti/update.log"
DJANGODIR=/var/www/rede_gsti
BRANCH="master"
SUPERVISOR_PROCESS="rede_gsti"
ENVIRONMENT="production"

DJANGO_SETTINGS_MODULE=rede_gsti.settings
DJANGO_WSGI_MODULE=rede_gsti.wsgi


cd $DJANGODIR
source $DJANGODIR/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
#pull the changes

git pull origin $BRANCH

# Getting current date
dt=$(date '+%d/%m/%Y %H:%M:%S');

#exporting environment
export PROJECT_ENVIRONMENT=$ENVIRONMENT

# Writing in log
echo "[$dt] - Pulling test and restartig..." >> $LOG_PATH

#Compiling messages
python manage.py compilemessages

# Running makemigrations merge if necessary
python manage.py makemigrations --merge

# Running Django migrate
python manage.py migrate >> $LOG_PATH

# Running Django collectstatic
python manage.py collectstatic -c --noinput >> $LOG_PATH

# Restarting
sudo supervisorctl restart $SUPERVISOR_PROCESS

# Writing the end of the process in log
echo "[$dt] - Done." >> $LOG_PATH
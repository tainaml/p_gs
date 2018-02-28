#!/bin/bash

# Declaring LOG and Branch vars
LOG_PATH="/var/log/rede_gsti/update.log"
BRANCH="master"
SUPERVISOR_PROCESS="rede_gsti"
ENVIRONMENT="production"
PROJECT_PATH="/var/www/rede_gsti"
VIRTUAL_ENV_DIR="$PROJECT_PATH/venv"

cd $PROJECT_PATH
source $VIRTUAL_ENV_DIR/bin/activate
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
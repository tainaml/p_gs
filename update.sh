#!/bin/bash

# Declaring LOG and Branch vars
LOG_PATH="/var/log/rede_gsti/update.log"
BRANCH="develop"
SUPERVISOR_PROCESS="rede_gsti"

#pull the changes
git pull origin $BRANCH

# Getting current date
dt=$(date '+%d/%m/%Y %H:%M:%S');

# Writing in log
echo "[$dt] - Pulling test and restartig..." >> $LOG_PATH

# Running Django migrate
python manage.py migrate >> $LOG_PATH

# Running Django collectstatic
python manage.py collectstatic -c --noinput >> $LOG_PATH

# Restarting
sudo supervisorctl restart $SUPERVISOR_PROCESS

# Writing the end of the process in log
echo "[$dt] - Done." >> $LOG_PATH

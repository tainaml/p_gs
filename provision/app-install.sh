#!/bin/bash

cd /var/www
sudo pip install -r requirements.txt
python manage.py migrate

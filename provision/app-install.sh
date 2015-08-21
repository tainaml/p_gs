#!/bin/bash

cd /var/www
pip install -r requirements.txt
python manage.py migrate

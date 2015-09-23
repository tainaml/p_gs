#!/usr/bin/env bash

cd /var/www

echo "[UP CELERY]"

# Thumbor UP
python manage.py celeryd_detach worker -B -l info -f celery.log
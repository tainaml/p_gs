#!/bin/bash

echo "[UPDATE WEB]"

cd /var/www

git submodule update --init --remote -f --rebase --merge --recursive

pip install --user -r requirements.txt

python manage.py makemigrations
python manage.py migrate
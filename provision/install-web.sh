#!/usr/bin/env bash

# Python dev packages
apt-get install -y build-essential python python-dev python-setuptools python-pip


# Dependencies for image processing with Pillow (drop-in replacement for PIL)
# supporting: jpeg, tiff, png, freetype, littlecms
apt-get install -y libjpeg-dev libtiff-dev zlib1g-dev libfreetype6-dev liblcms2-dev


# Translation rules
apt-get install -y gettext


# Postgresql
apt-get install -y libpq-dev


# virtualenv global setup
if ! command -v pip; then
    easy_install -U pip
fi
if [[ ! -f /usr/local/bin/virtualenv ]]; then
    easy_install virtualenv virtualenvwrapper stevedore virtualenv-clone
fi


# Cleanup
apt-get clean -y
#!/bin/bash

# Script to set up dependencies for Django on Vagrant.

PGSQL_VERSION=9.3

# Need to fix locale so that Postgres creates databases in UTF-8
cp -p /vagrant/provision/data/etc-bash.bashrc /etc/bash.bashrc
locale-gen en_GB.UTF-8
dpkg-reconfigure locales

export LANGUAGE=en_GB.UTF-8
export LANG=en_GB.UTF-8
export LC_ALL=en_GB.UTF-8

# Install essential packages from Apt
apt-get update -y

# Python dev packages
apt-get install -y build-essential python python-dev python-setuptools python-pip

# Dependencies for image processing with Pillow (drop-in replacement for PIL)
# supporting: jpeg, tiff, png, freetype, littlecms
apt-get install -y libjpeg-dev libtiff-dev zlib1g-dev libfreetype6-dev liblcms2-dev

# Git (we'd rather avoid people keeping credentials for git commits in the repo, but sometimes we need it for pip requirements that aren't in PyPI)
apt-get install -y git

# Translation rules
apt-get install -y gettext

# Postgresql
sudo sh /vagrant/provision/database.sh
apt-get install -y libpq-dev

# Thumbor
apt-get install -y python-pip build-dep python-opencv opencv-dev python-numpy python-dev
apt-get install -y ffmpeg libjpeg-dev libpng-dev libtiff-dev libjasper-dev libgtk2.0-dev
apt-get install -y python-numpy python-pycurl webp python-opencv python-dev


# virtualenv global setup
if ! command -v pip; then
    easy_install -U pip
fi
if [[ ! -f /usr/local/bin/virtualenv ]]; then
    easy_install virtualenv virtualenvwrapper stevedore virtualenv-clone
fi

# bash environment global setup
cp -p /vagrant/provision/data/bashrc /home/vagrant/.bashrc


# Cleanup
apt-get clean -y

# Upgrade
apt-get upgrade -y
apt-get clean

# Install RabbitMQ broker for Celery
apt-get -y install rabbitmq-server

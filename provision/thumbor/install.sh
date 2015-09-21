#!/bin/bash

apt-get update 
apt-get install -y build-essential python-dev curl python-pycurl python-pip
apt-get install -y python-numpy python-opencv webp libpng-dev libtiff-dev libjasper-dev libjpeg-dev
apt-get install -y libdc1394-22-dev libdc1394-22 libdc1394-utils
apt-get install -y gifsicle libgif-dev


pip install opencv-engine
pip install thumbor
pip install supervisor
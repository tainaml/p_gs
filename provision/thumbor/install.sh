#!/usr/bin/env bash



# Thumbor

apt-get update -y

apt-get -y install \
build-essential \
checkinstall \
gcc \
python \
python-dev \
python-pip \
python2.7-dev \
libssl-dev \
libcurl4-openssl-dev \
python-numpy \
python-opencv \
libopencv-dev \
libjpeg-dev \
libpng-dev \
libx264-dev \
libass-dev \
libvpx1 \
libvpx-dev \
libwebp-dev \
python-opencv \
webp \
gifsicle

apt-get install -y build-essential libgtk2.0-dev libjpeg-dev libtiff4-dev libjasper-dev libopenexr-dev
apt-get install -y cmake python-dev python-numpy python-tk libtbb-dev libeigen3-dev yasm libfaac-dev
apt-get install -y libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev
apt-get install -y libx264-dev libqt4-dev libqt4-opengl-dev sphinx-common texlive-latex-extra libv4l-dev
apt-get install -y libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libvtk5-qt4-dev

apt-get install -y build-essential python-dev curl python-pycurl python-pip
apt-get install -y python-numpy python-opencv opencv-dev webp libpng-dev libtiff-dev libjasper-dev libjpeg-dev
apt-get install -y libdc1394-22-dev libdc1394-22 libdc1394-utils

apt-get -y build-dep python-opencv

pip install pycurl numpy pyopencv thumbor

cp -f /vagrant/thumbor.conf /etc/thumbor.conf

read -d "" ThumborUpstart <<"EOF"
description "Thumbor image manipulation service"
author "Jason Ormand <jason.ormand1@gmail.com>"
start on startup
stop on shutdown
exec thumbor -c /etc/thumbor.conf
post-start script
    PID=`status thumbor | egrep -oi '([0-9]+)$' | head -n1`
    echo $PID > /var/run/thumbor.pid
end script
post-stop script
    rm -f /var/run/thumbor.pid
end script
EOF

sudo echo "$ThumborUpstart" > /etc/init/thumbor.conf && \
sudo chmod 755 /etc/init/thumbor.conf && \
init-checkconf /etc/init/thumbor.conf && \
initctl reload-configuration && \
sudo service thumbor start
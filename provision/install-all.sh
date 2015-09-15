#!/usr/bin/env bash

# Need to fix locale so that Postgres creates databases in UTF-8
cp -p /vagrant/provision/data/etc-bash.bashrc /etc/bash.bashrc
locale-gen en_GB.UTF-8
dpkg-reconfigure locales

export LANGUAGE=en_GB.UTF-8
export LANG=en_GB.UTF-8
export LC_ALL=en_GB.UTF-8


# Install essential packages from Apt
apt-get update -y


# Git (we'd rather avoid people keeping credentials for git commits in the repo, but sometimes we need it for pip requirements that aren't in PyPI)
apt-get install -y git


# bash environment global setup
cp -p /vagrant/provision/data/bashrc /home/vagrant/.bashrc


# Cleanup
apt-get clean -y
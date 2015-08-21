#!/bin/bash

# to build box:
cd ..
vagrant up
rm -f taguear.box
vagrant package --output taguear.box

# to install locally:
# vagrant box add taguear-box taguear.box

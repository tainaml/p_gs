#!/usr/bin/env bash

cd /vagrant

echo "[Services going up]"

# Thumbor UP
thumbor -c thumbor.conf &
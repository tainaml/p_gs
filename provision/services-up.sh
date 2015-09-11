#!/usr/bin/env bash

cd /var/www

echo "[Services going up]"

# Thumbor UP
thumbor -c thumbor.conf &
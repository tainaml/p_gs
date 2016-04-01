#!/bin/bash

echo ">> Starting ..."

echo ">> Deleting old migrations"
find . -path "*/migrations/*.p*" -not -name "__init__.py" -delete

echo ">> Done"
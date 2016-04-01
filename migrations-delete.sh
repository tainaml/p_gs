#!/bin/bash

echo ">> Starting ..."

echo ">> Deleting old migrations"
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

echo ">> Done"
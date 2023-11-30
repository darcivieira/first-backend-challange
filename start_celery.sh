#!/bin/bash

pip install pipenv

pipenv install --system

celery -A main.celery worker --concurrency=2 --loglevel=info  &

wait -n

exit $?

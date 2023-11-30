#!/bin/bash

pip install pipenv

pipenv install --system

gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80 &

wait -n

exit $?

#!/bin/bash
set -e

echo "Running database migrations..."
flask db upgrade

echo "Starting gunicorn..."
exec gunicorn --workers 4 --bind 0.0.0.0:8080 --timeout 120 run:app

#!/bin/sh

# Run Celery worker
celery -A app.celery worker --loglevel=INFO --detach --pidfile=''

# Run Celery Beat
celery -A app.celery beat --loglevel=INFO --detach --pidfile=''

celery -A app.celery control enable_events

gunicorn -b 0.0.0.0:5000 app:app

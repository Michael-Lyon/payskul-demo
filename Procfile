web: celery -A payskul worker -E -n myworker1@%h --loglevel=INFO --pool=prefork --concurrency=8 & python manage.py migrate && gunicorn payskul.wsgi

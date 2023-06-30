web: celery -A payskul worker -E -n myworker1@%h --loglevel=INFO --pool=prefork --concurrency=8 --pidfile= --loglevel=info -E & python manage.py migrate && gunicorn payskul.wsgi

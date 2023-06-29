web: celery -A payskul worker  -E -n  --pool=prefork --concurrency=8 --loglevel=INFO & python manage.py migrate &&  gunicorn payskul.wsgi

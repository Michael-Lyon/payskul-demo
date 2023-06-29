web:  celery -A payskul worker -E -n  --pool=prefork --concurrency=8  & python manage.py migrate &&  gunicorn payskul.wsgi

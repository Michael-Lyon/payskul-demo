web:  celery -A payskul worker --pool=prefork --concurrency=8 -E -n & python manage.py migrate &&  gunicorn payskul.wsgi

web:  celery -A payskul worker --pool=prefork --concurrency=8 -E & python manage.py migrate &&  gunicorn payskul.wsgi

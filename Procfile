web: celery -A payskul worker --uid=michaellyon -E -n  --pool=prefork --concurrency=8  & python manage.py migrate &&  gunicorn payskul.wsgi

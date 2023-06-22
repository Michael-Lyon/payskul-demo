web: python manage.py migrate && gunicorn payskul.wsgi
worker: celery --app=payskul worker -l INFO
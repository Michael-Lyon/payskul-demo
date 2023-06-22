import os

from celery import Celery

# CELERY SETTINGS
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payskul.settings')
app = Celery('payskul', broker="redis://default:7MvsvYWMYnkcPRzaIiQK@containers-us-west-116.railway.app:5999")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

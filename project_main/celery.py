import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_main.settings')
app = Celery('celery')
app.config_from_object('django.conf:settings')
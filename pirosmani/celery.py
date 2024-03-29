from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from pirosmani.settings import CELERY_BROKER_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pirosmani.settings.base')
app = Celery('pirosmani', broker=CELERY_BROKER_URL, backend=CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # can we indicate specific apps insted of all: lambda: settings.INSTALLED_APPS

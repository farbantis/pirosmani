import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pirosmani',
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['localhost', '191.96.53.71', 'qimeer.online', '.qimeer.online']

# CELERY SETTINGS
broker_url = 'redis://191.96.53.71:6379/0'  # Use Redis on the VPS server
result_backend = 'redis://191.96.53.71:6379/0'  # Use Redis on the VPS server


import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

ALLOWED_HOSTS = ['localhost', os.getenv('ALLOWED_HOSTS_IP'), 'qimeer.online', '.qimeer.online']

# CELERY SETTINGS
broker_url = os.getenv('broker_url')  # Use Redis on the VPS server
result_backend = os.getenv('result_backend')  # Use Redis on the VPS server

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_HTTPONLY = False

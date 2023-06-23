from pathlib import Path
from .base import INSTALLED_APPS, MIDDLEWARE
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = True
INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
INTERNAL_IPS = ["127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CELERY_BROKER_URL = 'redis://localhost'  # Use Redis on the local machine
CELERY_RESULT_BACKEND = 'redis://localhost'  # Use Redis on the local machine

# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379
# REDIS_DB = 0

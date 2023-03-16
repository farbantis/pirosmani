from pathlib import Path
from .base import INSTALLED_APPS, MIDDLEWARE
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = True
INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CELERY SETTINGS

broker_url = 'redis://localhost'  # Use Redis on the local machine
result_backend = 'redis://localhost'  # Use Redis on the local machine


# ALLOWED_HOSTS = ['localhost', '127.0.0.1']
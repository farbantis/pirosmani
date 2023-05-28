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

# broker_url = 'redis://localhost'  # Use Redis on the local machine
# result_backend = 'redis://localhost'  # Use Redis on the local machine


ALLOWED_HOSTS = ['localhost', '127.0.0.1']
REDIS_HOST = 'localhost'  # Replace with your Redis host
REDIS_PORT = 6379  # Replace with your Redis port
REDIS_DB = 0  # Replace with your Redis database number

# Create a Redis connection pool
# REDIS_POOL = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }

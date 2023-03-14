from .base import *
import os
from pirosmani.celery import app as celery_app

__all__ = ('celery_app',)

if os.environ.get('ENV_NAME') == 'Production':
    from .production import *
elif os.environ.get('ENV_NAME') == 'Development':
    from .development import *

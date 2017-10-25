"""DEV server settings"""

from .base import * #pylint:disable=wildcard-import,unused-wildcard-import

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': get_env_variable('PGHOST'),
        'NAME': get_env_variable('PGDATABASE'),
        'USER': get_env_variable('PGUSER'),
        'PASSWORD': get_env_variable('PGPASSWORD'),
    }
}

STATIC_ROOT = '/home/django/api/api/static/'
MEDIA_ROOT = '/home/django/api/api/uploads/'

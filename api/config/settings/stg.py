"""Staging environment settings"""

from .base import * #pylint:disable=wildcard-import,unused-wildcard-import

DEBUG = True

URL_UPLOAD = 'http://dev-api.sucroo.com/upload/'
MEDIA_ROOT = '/home/django/django_project/api/uploads/'
STATIC_ROOT = '/home/django/django_project/api/static/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': get_env_variable('PGHOST'),
        'NAME': get_env_variable('PGDATABASE'),
        'USER': get_env_variable('PGUSER'),
        'PASSWORD': get_env_variable('PGPASSWORD'),
    }
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/home/django/django_project/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

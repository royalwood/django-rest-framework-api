"""Production environment settings"""

from .base import * #pylint:disable=wildcard-import,unused-wildcard-import

DEBUG = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

INSTALLED_APPS = (
    'opbeat.contrib.django',
)

MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
)

# OpBeat account - need a new account created for UCROO @ opbeat.com
# OPBEAT = {
#    'ORGANIZATION_ID': '389c4f770f8148fbbaaa026bbbe610fa',
#    'APP_ID': 'cf510c4793',
#    'SECRET_TOKEN': '9f2bdce81de83f4f5d7596d23f9d38ee755eeaaf',
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': get_env_variable('PGHOST'),
        'NAME': get_env_variable('PGDATABASE'),
        'USER': get_env_variable('PGUSER'),
        'PASSWORD': get_env_variable('PGPASSWORD'),
    }
}

STATIC_ROOT = '/home/django/django_project/api/static/'
MEDIA_ROOT = '/home/django/django_project/api/uploads/'

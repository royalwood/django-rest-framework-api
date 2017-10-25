"""Settings for local development environment"""

from .base import * #pylint:disable=wildcard-import,unused-wildcard-import

DEBUG = True

URL_UPLOAD = 'http://127.0.0.1:8000/upload/'
MEDIA_ROOT = '/Users/ncole/Documents/UCROO/UCROO_API/uploads/'
STATIC_ROOT = '/Users/ncole/Documents/UCROO/UCROO_API/static/'


# Send Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.mailgun.org"
EMAIL_HOST_USER = "django-dev@sucroo.com"
EMAIL_HOST_PASSWORD = "ks9dsk9@*@J!"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': get_env_variable('PGHOST'),
        'NAME': get_env_variable('PGDATABASE'),
        'USER': get_env_variable('PGUSER'),
        'PASSWORD': get_env_variable('PGPASSWORD'),
    }
}

ALLOWED_HOSTS += ('localhost', '127.0.0.1', )

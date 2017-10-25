"""Base settings for all environments"""
import os

from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured


admin.site.site_header = 'Ucroo Staff Admin'

def get_env_variable(var_name):
    """Get the environment variable"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)

ALLOWED_HOSTS = ['backend.sucroo.com', 'backend.ucroo.com', 'dev-api.sucroo.com', '138.68.24.137', '138.197.201.179',]
APPEND_SLASH = False
AUTH_USER_MODEL = "users.User"
AXES_COOLOFF_TIME = 1
AXES_LOCK_OUT_AT_FAILURE = True
AXES_LOGIN_FAILURE_LIMIT = 5
AXES_USERNAME_FORM_FIELD = 'email'
AXES_USE_USER_AGENT = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.mailgun.org"
EMAIL_HOST_PASSWORD = "ks9dsk9@*@J!"
EMAIL_HOST_USER = "django-dev@sucroo.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
FILE_UPLOAD_PERMISSIONS = 0o644
LANGUAGE_CODE = 'en-us'
MEDIA_URL = '/uploads/'
ROOT_URLCONF = 'config.urls'
SECRET_KEY = get_env_variable('SECRET_KEY')
SITE_ID = 1 # For django-activity-stream and others
STATIC_URL = '/static/'
TIME_ZONE = 'UTC'
TWILIO_ACCOUNT_SID='AC3bdc1772a9c4a7a8bd7094fe98c4d51c'
TWILIO_AUTH_TOKEN=get_env_variable('TWILIO_AUTH_TOKEN')
TWILIO_FROM='+17853674411'
USE_I18N = True
USE_L10N = True
USE_TZ = True
WSGI_APPLICATION = 'config.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django_auth_adfs': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    # 'LTI',
    # 'django_auth_adfs',
    'rest_framework',
    'rest_framework_docs',
    'corsheaders',
    'import_export',
    'axes',
    'actstream',
    # Our apps
    'activity',
    'conversations',
    'core',
    'subjects',
    'feeds',
    'groups',
    'karma',
    'keywords',
    'marketplace',
    'notifications',
    'search',
    'studentcalendar',
    'studytimer',
    'universities',
    'upload_file',
    'users',
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    # Auth User
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        # 'django_auth_adfs.backend.AdfsBackend',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'django_auth_adfs.middleware.LoginRequiredMiddleware',
)

# CORS for AngularJS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'localhost',
    'localhost:3000',
    '127.0.0.1',
    'dev.sucroo.com',
    'sucroo.com',
    'ucroo.com',
)
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)
CORS_EXPOSE_HEADERS = (
    'content-type',
    'accept',
    'origin',
    'authorization'
)

# ADFS AUTH - dynamic based on provider for UCROO Sass Instance
#AUTHENTICATION_BACKENDS = (
#    'django_auth_adfs.backend.AdfsBackend',
#)
#
#AUTH_ADFS = {
#    "ADFS_SERVER": "adfs.yourcompany.com",
#    "ADFS_CLIENT_ID": "your-configured-client-id",
#    "ADFS_RESOURCE": "your-adfs-RPT-name",
#    "ADFS_SIGNING_CERT": "/path/to/adfs-signing-certificate.pem",
#    # Make sure to read the documentation about the ADFS_AUDIENCE setting
#    # when you configured the identifier as a URL!
#    "ADFS_AUDIENCE": "microsoft:identityserver:your-RelyingPartyTrust-identifier",
#    "ADFS_ISSUER": "http://adfs.yourcompany.com/adfs/services/trust",
#    "ADFS_CA_BUNDLE": "/path/to/ca-bundle.pem",
#    "ADFS_CLAIM_MAPPING": {"first_name": "given_name",
#                           "last_name": "family_name",
#                           "email": "email"},
#    "ADFS_REDIR_URI": "https://www.yourcompany.com/oauth2/login",
#    "LOGIN_EXEMPT_URLS": ["universities/", "public/"],
#}

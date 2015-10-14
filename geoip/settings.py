"""
Django settings for the <projectname> project.

The settings are organized similarly to the list at
https://docs.djangoproject.com/en/1.8/ref/settings/#core-settings-topical-index

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
import os
from django.utils.translation import ugettext_lazy as _


# Set project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#########
# Cache #
#########

# Caching backends
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


############
# Database #
############

# Database backends
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('GEOIP_DB_NAME'),
        'USER': os.getenv('GEOIP_DB_USER'),
        'PASSWORD': os.getenv('GEOIP_DB_PASSWORD'),
        'HOST': os.getenv('GEOIP_DB_HOST', 'localhost'),
        'PORT': os.getenv('GEOIP_DB_PORT', '5432'),
    }
}


#############
# Debugging #
#############

# Debugging
DEBUG = str(os.getenv('GEOIP_DEBUG_MODE', False)).lower() == "true"

# Propagate exceptions
DEBUG_PROPAGATE_EXCEPTIONS = False


#########
# Email #
#########

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('GEOIP_EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.getenv('GEOIP_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('GEOIP_EMAIL_PASSWORD')
EMAIL_PORT = '465'
EMAIL_USE_TLS = True

# Server email
SERVER_EMAIL = 'noreply@jjkester.nl'

# Default sender
DEFAULT_FROM_EMAIL = 'noreply@jjkester.nl'

# Subject prefix
EMAIL_SUBJECT_PREFIX = ''


###################
# Error reporting #
###################

# Admins and managers
ADMINS = ()
MANAGERS = ()

# Silence system checks to avoid log spam
SILENCED_SYSTEM_CHECKS = []


#########
# Files #
#########

# Static file location
STATIC_ROOT = os.getenv('GEOIP_STATIC_ROOT')
STATIC_URL = '/static/'

# Uploaded file location
MEDIA_ROOT = os.getenv('GEOIP_MEDIA_ROOT')
MEDIA_URL = '/media/'


#################
# Globalization #
#################

# Use internationalization/localization/timezones
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Available languages
LANGUAGES = (
    ('en', _("English")),
)

# Defaults
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'

# Cookie settings
LANGUAGE_COOKIE_NAME = 'language'


########
# HTTP #
########

# Middleware
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

# Block user agents
DISALLOWED_USER_AGENTS = []

# Browser settings
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = True

# HTTP Strict Transport Security
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False

# Proxy configuration
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


###########
# Logging #
###########

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.getenv('GEOIP_LOG_FILE'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}


##########
# Models #
##########

# Apps
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'bootstrapform',
    'djcelery',

    'geodb',

    'geoip.databases',
    'geoip.nodes',
    'geoip.measurements',
    'geoip.scrapers',
)

# User model
AUTH_USER_MODEL = 'auth.User'


############
# Security #
############

# Valid hostnames
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'geoip.jjkester.nl']

# Internal IPs
INTERNAL_IPS = []

# Cryptographic signing
SIGNING_BACKEND = 'django.core.signing.TimestampSigner'
SECRET_KEY = os.getenv('GEOIP_SECRET_KEY')

# Cross Site Request Forgery
CSRF_COOKIE_NAME = 'csrf'
CSRF_COOKIE_HTTPONLY = True


############
# Sessions #
############

# Session engine
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Misc
SESSION_SAVE_EVERY_REQUEST = True

# Cookie settings
SESSION_COOKIE_NAME = 'session'
SESSION_COOKIE_HTTPONLY = True


#############
# Templates #
############

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ),
            'debug': DEBUG,
        },
    },
]


########
# URLs #
########

# URL formatting
PREPEND_WWW = False
APPEND_SLASH = True

# Root URL configuration
ROOT_URLCONF = 'geoip.urls'


###########
# Plugins #
###########

# Celery
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

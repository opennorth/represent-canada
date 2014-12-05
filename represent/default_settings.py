# coding: utf-8
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# @see https://docs.djangoproject.com/en/1.5/topics/i18n/translation/
from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.i18n',
)
TEMPLATE_LOADERS = global_settings.TEMPLATE_LOADERS + (
    'django.template.loaders.eggs.Loader',
)
MIDDLEWARE_CLASSES = global_settings.MIDDLEWARE_CLASSES + (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.gis',
    'django_extensions',
    'boundaries',
    'representatives',
    'postcodes',
    'finder',
]

# Represent's current functionality isn't a good fit for fake-Host-header
# attacks, so this shouldn't be a security risk. You may want to include
# a real ALLOWED_HOSTS setting in settings.py, though.
ALLOWED_HOSTS = ['*']
SECRET_KEY = '+t(q+ljogaj(+7m@kueu-g881gb8xp_oaz)$iabxjp8a1@2#u!'
TIME_ZONE = 'America/Montreal'
LANGUAGE_CODE = 'en'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
ROOT_URLCONF = 'represent.urls'
WSGI_APPLICATION = 'represent.wsgi.application'

LANGUAGES = (
    ('en', 'English'),
    ('fr', 'Français'),
)

REPRESENTATIVES_ENABLE_CANDIDATES = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'boundaries': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

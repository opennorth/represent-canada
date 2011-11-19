#!/usr/bin/env python

from config.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Use pgpool
DATABASES['default']['PORT'] = '5433'

# Static media
STATIC_ROOT = '/mnt/media/hacktyler_boundaryservice'

# Uploads 
MEDIA_ROOT = '/mnt/uploads/hacktyler_boundaryservice' 

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Django-compressor
COMPRESS_ENABLED = True


from config.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Database
DATABASES['default']['HOST'] = 'db.hacktyler.com'
DATABASES['default']['PORT'] = '5433'
DATABASES['default']['USER'] = 'boundaryservice'
DATABASES['default']['PASSWORD'] = 'dMQlbUCftr'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://media.hacktyler.com/boundaryservice/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'http://media.hacktyler.com/boundaryservice/admin_media/'

# Predefined domain
MY_SITE_DOMAIN = 'boundaryservice.hacktyler.com'

# Email
EMAIL_HOST = 'mail.hacktyler.com'
EMAIL_PORT = 25

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'cache.hacktyler.com:11211',
    }
}

# S3
AWS_S3_URL = 's3://media.hacktyler.com/boundaryservice/'

# Internal IPs for security
INTERNAL_IPS = ()

API_DOMAIN = 'boundaryservice.hacktyler.com'

# logging
import logging.config
LOG_FILENAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logger.conf')
logging.config.fileConfig(LOG_FILENAME)


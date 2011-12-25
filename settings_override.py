try:
    from settings_database import *
except ImportError:
    pass
    
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
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
            'level': 'WARNING',
        }
    }
}

EXAMPLE_SCOPE = 'Canada'
EXAMPLE_BOUNDARY_SET = 'Federal Electoral District'
EXAMPLE_BOUNDARY_SETS = 'Federal Electoral Districts' # plural
EXAMPLE_BOUNDARY_SET_CODE = 'federal'
EXAMPLE_BOUNDARY_SET_CODE_BIS = 'example-boundary-set-b' # "bis" is latin for "again"
EXAMPLE_BOUNDARY_SET_RESPONSE = """
{
    "authority": "Her Majesty the Queen in Right of Canada",
    "boundaries": [
        "/1.0/boundary/abbotsford-.../",
        "/1.0/boundary/abitibi-baie-james-nunavik-eeyou-.../",
        "/1.0/boundary/abitibi-temiscamingue-.../",
        ...
    ],
    "count": 308,
    "domain": "Canada",
    "href": "http://www12.statcan.gc.ca/census-recensement/...",
    "last_updated": "2011-11-28",
    "metadata_fields": [
        "FEDUID",
        "FEDNAME",
        "FEDENAME",
        "FEDFNAME",
        "PRUID",
        "PRNAME"
    ],
    "name": "Federal Electoral Districts",
    "notes": "",
    "resource_uri": "/1.0/boundary-set/federal-electoral-districts/",
    "slug": "federal-electoral-districts"
}"""
EXAMPLE_BOUNDARY = 'Ottawa - Vanier'
EXAMPLE_BOUNDARY_CODE = '35065'
EXAMPLE_BOUNDARY_RESPONSE = """
{
    "centroid": {
        "coordinates": [-75.64011961416415, 45.44439004432772],
        "type": "Point"
    },
    "external_id": "35065",
    "kind": "Federal Electoral District"
     "metadata": {
        "FEDENAME": "Ottawa - Vanier",
        "FEDFNAME": "Ottawa - Vanier",
        "FEDNAME": "Ottawa - Vanier",
        "FEDUID": "35065",
        "PRNAME": "Ontario",
        "PRUID": "35"
    },
    "name": "Ottawa - Vanier",
    "resource_uri": "/1.0/boundary/ottawa-vanier-federal-electoral-district/",
    "set": "/1.0/boundary-set/federal-electoral-districts/",
    "simple_shape": {
        "coordinates": [[[
            [-75.695098951, 45.424781456000105],
            [-75.699035784, 45.42691838000012],
            [-75.70377828199999, 45.42984379800008],
            ...
        ]]],
        "type": "MultiPolygon"
    },
    "slug": "ottawa-vanier-federal-electoral-district"
}"""
EXAMPLE_PLACE = '24 Sussex Drive, Ottawa'
EXAMPLE_PLACE_LAT_LNG = '45.444369,-75.693832'
EXAMPLE_UNIT = 'kilometre'
EXAMPLE_UNIT_CODE = 'km'

COMPRESS_ENABLED = False 

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

API_DOMAIN = '127.0.0.1:8000'
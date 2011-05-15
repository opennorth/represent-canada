"""
Configuration describing the shapefiles to be loaded.
"""
from datetime import date

from django.contrib.humanize.templatetags.humanize import ordinal

import utils

SHAPEFILES = {
    # This key should be the plural name of the boundaries in this set
    'City Council Districts': {
        # Path to a shapefile, relative to /data/shapefiles
        'file': 'city_council_districts/Council Districts.shp',
        # Generic singular name for an boundary of from this set
        'singular': 'City Council District',
        # Should the singular name come first when creating canonical identifiers for this set?
        'kind_first': False,
        # Function which each feature wall be passed to in order to extract its "external_id" property
        # The utils module contains several generic functions for doing this
        'ider': utils.simple_namer(['DISTRICT']),
        # Function which each feature will be passed to in order to extract its "name" property
        'namer': utils.simple_namer(['NAME']),
        # Authority that is responsible for the accuracy of this data
        'authority': 'Tyler GIS Department',
        # Geographic extents which the boundary set encompasses
        'domain': 'Tyler',
        # Last time the source was checked for new data
        'last_updated': date(2011, 5, 14),
        # A url to the source of the data
        'href': 'http://www.smithcountymapsite.org/webshare/data.html',
        # Notes identifying any pecularities about the data, such as columns that were deleted or files which were merged
        'notes': '',
        # Encoding of the text fields in the shapefile, i.e. 'utf-8'. If this is left empty 'ascii' is assumed
        'encoding': '',
        # SRID of the geometry data in the shapefile if it can not be inferred from an accompanying .prj file
        # This is normally not necessary and can be left undefined or set to an empty string to maintain the default behavior
        'srid': ''
    },
    'Justice of the Peace Precincts': {
        'file': 'justice_peace_precincts/JP.shp',
        'singular': 'Justice of the Peace Precinct',
        'kind_first': True,
        'ider': utils.simple_namer(['JP']),
        'namer': utils.simple_namer(['JP']),
        'authority': 'Smith County',
        'domain': 'Smith County',
        'last_updated': date(2011, 5, 14),
        'href': 'http://www.smithcountymapsite.org/webshare/data.html',
        'notes': '',
        'encoding': '',
        'srid': ''
    },
    'Commissioners Court Precincts': {
        'file': 'commissioners_court_precincts/COMM.shp',
        'singular': 'Commissioners Court Precinct',
        'kind_first': True,
        'ider': utils.simple_namer(['COMMISSION']),
        'namer': utils.simple_namer(['COMMISSION']),
        'authority': 'Smith County',
        'domain': 'Smith County',
        'last_updated': date(2011, 5, 14),
        'href': 'http://www.smithcountymapsite.org/webshare/data.html',
        'notes': '',
        'encoding': '',
        'srid': ''
    },
}

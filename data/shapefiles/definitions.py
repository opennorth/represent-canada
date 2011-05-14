"""
Configuration describing the shapefiles to be loaded.
"""
from datetime import date

from django.contrib.humanize.templatetags.humanize import ordinal

import utils

SHAPEFILES = {
    # This key should be the plural name of the boundaries in this set
    'Neighborhoods': {
        # Path to a shapefile, relative to /data
        'file': 'neighborhoods/Neighboorhoods.shp',
        # Generic singular name for an boundary of from this set
        'singular': 'Neighborhood',
        # Should the singular name come first when creating canonical identifiers for this set?
        # (e.g. True in this case would result in "Neighborhood South Austin" rather than "South Austin Neighborhood")
        'kind_first': False,
        # Function which each feature wall be passed to in order to extract its "external_id" property
        # The utils module contains several generic functions for doing this
        'ider': utils.simple_namer(['PRI_NEIGH_']),
        # Function which each feature will be passed to in order to extract its "name" property
        'namer': utils.simple_namer(['PRI_NEIGH']),
        # Authority that is responsible for the accuracy of this data
        'authority': 'City of Chicago',
        # Geographic extents which the boundary set encompasses
        'domain': 'Chicago',
        # Last time the source was checked for new data
        'last_updated': date(2010, 12, 12),
        # A url to the source of the data
        'href': 'http://www.cityofchicago.org/city/en/depts/doit/supp_info/gis_data.html',
        # Notes identifying any pecularities about the data, such as columns that were deleted or files which were merged
        'notes': '',
        # Encoding of the text fields in the shapefile, i.e. 'utf-8'. If this is left empty 'ascii' is assumed
        'encoding': ''
        # SRID of the geometry data in the shapefile if it can not be inferred from an accompanying .prj file
        # This is normally not necessary and can be left undefined or set to an empty string to maintain the default behavior
        #'srid': ''
    },
}

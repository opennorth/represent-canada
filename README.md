The Newsapps Boundary Service is a ready-to-deploy system for aggregating regional boundary data (from shapefiles) and republishing via a RESTful JSON API. It is packaged as a pluggable Django application so that it can be easily integrated into any project.

This project allows you to easily create sites like [You are here.](http://boundaries.tribapps.com/) and [Smith County Boundaries](http://boundaryservice.hacktyler.com/).

# Getting Started

First, install the requirements. This assumes you already have Python 2.7.

    sudo easy_install pip
    sudo pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Next, create a PostgreSQL database, as the Boundary Service depends on PostGIS.

    DB=EXAMPLE_DB_NAME
    createdb -h localhost $DB
    createlang -h localhost plpgsql $DB

To spatially-enable the database, you must load PostGIS definitions files. You can use `locate` (Linux) or `mdfind` (OS X) to find these files.

    psql -h localhost -d $DB -f postgis.sql
    psql -h localhost -d $DB -f spatial_ref_sys.sql

It may be worthwhile to [create a template database](http://www.bigfastblog.com/landsliding-into-postgis-with-kml-files) if you will be creating many PostGIS databases.

Lastly, configure the `DATABASES` Django setting and and create the database tables.

    cp settings_override.py.example settings_override.py
    vi settings_override.py
    python manage.py syncdb

You can now copy `definitions.py.example` to start adding your geospatial data:

    cp data/shapefiles/definitions.py.example data/shapefiles/definitions.py

# Adding geospatial data

Add your geospatial data to `data/shapefiles`. It may be a zipfile or a directory containing a shp, shx, dbf, prj. Then, fill in `definitions.py`. Note that the keys of the `SHAPEFILES` dictionary and the value of the `singular` key should be ASCII.

Then, run `python manage.py loadshapefiles`. Note that this command will import everything under `data/shapefiles`. If you're already run this command once, then you'll want to specify which data to import. You can include (whitelist) data for import:

    python manage.py loadshapefiles -o KeyA,KeyB,...

Or exclude (blacklist) data for import:

    python manage.py loadshapefiles -e KeyA,KeyB,...

__Important Note:__ The comma-separated arguments are the keys of the `SHAPEFILES` dictionary with spaces removed.

If you want to reset the database and start over, run:

    python manage.py loadshapefiles -c

If that doesn't work you can always do:

    python manage.py sqlreset boundaryservice | psql -h localhost DB_NAME

# Development

To test it locally:

    python manage.py runserver
    curl http://127.0.0.1:8000/1.0/

# Customization

To localize the sample boundary sets, etc. edit these two files:

* Go through the `@todo` in `finder.js`
* Edit `EXAMPLE_*` in `settings_override.py`

# Deployment

* Configure `CACHES` in `settings_override.py`
* Set `COMPRESS_ENABLED = True` in `settings_override.py`

# Troubleshooting

If `python manage.py runserver` quits unexpectedly without error, use an alternative server:

    pip install gunicorn
    python manage.py collectstatic
    gunicorn_django settings.py

If `python manage.py loadshapefiles` causes this error:

    ERROR 1: dlopen(/Library/Application Support/GDAL/1.8/PlugIns/ogr_GRASS.dylib, 1): Symbol not found: __ZN11OGRSFDriver14CopyDataSourceEP13OGRDataSourcePKcPPc
      Referenced from: /Library/Application Support/GDAL/1.8/PlugIns/ogr_GRASS.dylib
      Expected in: flat namespace
     in /Library/Application Support/GDAL/1.8/PlugIns/ogr_GRASS.dylib

you may resolve it on OS X by running:

    brew install gdal-grass

If `python manage.py loadshapefiles` causes this error:

    IOError: [Errno 2] No such file or directory: '/var/folders/yn/4cwyp7v55w1c127fbn8sk8gm0000gn/...'

make sure that all files referenced in `definitions.py` exist.

# Contributing

* [Newsapps Boundary Services issues](https://github.com/newsapps/django-boundaryservice/issues?sort=created&direction=desc&state=open)

# Attribution

This Boundary Service instance uses the following open-source software:

* [Newsapps Boundary Service](https://github.com/newsapps/django-boundaryservice)
* [Leaflet](http://leaflet.cloudmade.com/)
* [json2.js](https://github.com/douglascrockford/JSON-js)
* [store.js](https://github.com/marcuswestin/store.js)
* [Less Framework 3](http://lessframework.com/v3/)
* [Eric Meyer Reset CSS](http://meyerweb.com/eric/tools/css/reset/)
* [Modernizr from HTML5 Boilerplate](http://html5boilerplate.com/)

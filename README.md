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

Lastly, configure the `DATABASES` Django setting.

    cp settings_override.py.example settings_override.py
    vi settings_override.py

# Customization

To localize the sample boundary sets, etc. edit these two files:

* Go through the `@todo` in `finder.js`
* Edit `EXAMPLE_*` in `settings_override.py`

# Deployment

* Configure `CACHES` in `settings_override.py`
* Set `COMPRESS_ENABLED = True` in `settings_override.py`

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

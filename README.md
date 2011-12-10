# Getting Started

    DB=EXAMPLE_DB_NAME
    sudo pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    createdb -h localhost $DB
    createlang -h localhost plpgsql $DB

To spatially-enable the database, you must load PostGIS definitions files. You can use `locate` (Linux) or `mdfind` (OS X) to find these files.

    psql -h localhost -d $DB -f postgis.sql
    psql -h localhost -d $DB -f spatial_ref_sys.sql

* Configure `DATABASE` in `settings.py`

# Customization

* Go through `@todo` in `finder.js`
* Edit Examples in `settings.py`

# Deployment

* Configure `CACHES` and `STATIC_ROOT` in `settings.py`
* Set `COMPRESS_ENABLED = True` in `settings.py`

# Attribution

* [Newsapps Boundary Service](https://github.com/newsapps/django-boundaryservice)
* [Leaflet](http://leaflet.cloudmade.com/)
* [json2.js](https://github.com/douglascrockford/JSON-js)
* [store.js](https://github.com/marcuswestin/store.js)
* [Less Framework 3](http://lessframework.com/v3/)
* [Eric Meyer Reset CSS](http://meyerweb.com/eric/tools/css/reset/)
* [Modernizr from HTML5 Boilerplate](http://html5boilerplate.com/)
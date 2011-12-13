The Canada Boundary Service aggregates regional boundary data (from shapefiles) and republishes this data via a RESTful JSON API.

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

    cp settings_database.py.example settings_database.py
    vi settings_database.py
    python manage.py syncdb

# Adding Data

Because the licenses for the digital boundary files are unclear, this data is currently held in a private repository. The `definitions.py` file includes URLs to these files if publicly available. Please contact [james@opennorth.ca](mailto:james@opennorth.ca) to contribute new shapefiles.

# Upstream Changes

Canada Boundary Service is a fork of [Blank Boundary Service](https://github.com/opennorth/blank-boundaryservice). To pull in upstream changes, first add an upstream endpoint:

    git remote add upstream git://github.com/opennorth/blank-boundaryservice.git

Now, you can pull in upstream changes ([as documented by GitHub](http://help.github.com/fork-a-repo/)):

    git fetch upstream
    git merge upstream/master

Additional documentation is available from the [Blank Boundary Service README](https://github.com/opennorth/blank-boundaryservice#readme).

# Contact

Please contact [james@opennorth.ca](mailto:james@opennorth.ca) for all questions or comments. Please submit feature requests, bug fixes, etc. [through GitHub](https://github.com/opennorth/canada-boundaryservice/issues).

[Represent](http://represent.opennorth.ca) is the open database of Canadian elected officials and electoral districts. It provides a [REST API](http://represent.opennorth.ca/api/) to boundary, representative, and postcode resources.

This repository contains a master Django project, documentation, and a demo app. Code for the individual components of the API is in separate packages, which this project depends on:

* [represent-boundaries](http://github.com/rhymeswithcycle/represent-boundaries)
* [represent-reps](http://github.com/rhymeswithcycle/represent-reps)
* [represent-postcodes](http://github.com/rhymeswithcycle/represent-postcodes)

While the Canada site doesn't currently use it, there's a plugin project to provide colourful district map tiles:

* [represent-maps](http://github.com/tauberer/represent-maps)

# Getting Started

The following instructions are to setup your own instance of Represent. If you just want access to data, [please read our API documentation](http://represent.opennorth.ca/api/).

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

    cp settings.py.example settings.py
    $EDITOR settings.py
    python manage.py syncdb
    python manage.py migrate

You can launch a development server with:

    python manage.py runserver

# Adding Data

[Download the data](https://github.com/opennorth/represent-canada-data), and then symlink `represent-canada-data` into the project directory:

    mkdir data
    ln -s /path/to/represent-canada-data/ data/shapefiles

To load the data into the API, see the documentation for the boundaries, representatives, and postcodes packages.

# International Use

Apart from the postcode component, which is optional and simple to rewrite, we've tried to avoid any Canada-specific code in this project. We hope reusing our code isn't too difficult, and would love to hear about international project using this code.

# Contact

Please use [GitHub Issues](http://github.com/opennorth/represent-canada/issues) for bug reports, feature requests, etc. You may also contact [represent@opennorth.ca](mailto:represent@opennorth.ca).

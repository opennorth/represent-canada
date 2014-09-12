# Represent

[![Dependency Status](https://gemnasium.com/opennorth/represent-canada.png)](https://gemnasium.com/opennorth/represent-canada)

[Represent](http://represent.opennorth.ca) is the open database of Canadian elected officials and electoral districts. It provides a [REST API](http://represent.opennorth.ca/api/) to boundary, representative, and postcode resources.

This repository contains a master Django project, documentation, and a demo app. Code for the individual components of the API is in separate packages, which this project depends on:

* [represent-boundaries](http://github.com/rhymeswithcycle/represent-boundaries)
* [represent-reps](http://github.com/rhymeswithcycle/represent-reps)
* [represent-postcodes](http://github.com/rhymeswithcycle/represent-postcodes)

While the Canada site doesn't currently use it, there's a plugin project to provide colourful district map tiles:

* [represent-maps](http://github.com/tauberer/represent-maps)

## Getting Started

The following instructions are to setup your own instance of Represent. If you just want access to data, [please read our API documentation](http://represent.opennorth.ca/api/).

Follow the instructions in the [Python Quick Start Guide](https://github.com/opennorth/opennorth.ca/wiki/Python-Quick-Start%3A-OS-X) to install Homebrew, Git, Python, virtualenv, GDAL and PostGIS.

Create a database using the PostGIS template:

    createdb -h localhost boundaryservice -T template_postgis

Install the project:

    mkvirtualenv represent
    git clone git://github.com/opennorth/represent-canada.git
    cd represent-canada
    pip install -r requirements.txt

Configure the `DATABASES` Django setting and and create the database tables:

    cp settings.py.example settings.py
    $EDITOR settings.py
    python manage.py syncdb
    python manage.py migrate

You can launch a development server with:

    python manage.py runserver

## Adding Data

[Download the data](https://github.com/opennorth/represent-canada-data), and then symlink `represent-canada-data` into the project directory:

    mkdir data
    ln -s /path/to/represent-canada-data/ data/shapefiles

To load the data into the API, see the documentation for the boundaries, representatives, and postcodes packages.

## International Use

Apart from the postcode component, which is optional and simple to rewrite, we've tried to avoid any Canada-specific code in this project. We hope reusing our code isn't too difficult, and would love to hear about international project using this code.

## Contact

Please use [GitHub Issues](http://github.com/opennorth/represent-canada/issues) for bug reports, feature requests, etc. You may also contact [represent@opennorth.ca](mailto:represent@opennorth.ca).

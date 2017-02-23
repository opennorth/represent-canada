# Deployment

## Servers

Represent and [openparliament.ca](https://openparliament.ca/) currently share two: a large dedicated server, `alpheus`, and a smaller virtual server, `tempeh`. The servers are configured identically, except that PostgreSQL on `tempeh` has streaming replication set up with `alpheus` (meaning that the Represent database on `tempeh` is read-only). If `alpheus` goes down, Represent fails over to `tempeh` ([see below](#dns)). The servers run Nginx, PostgreSQL 9.6, PostGIS 2.3, and Memcached.

This directory contains some server configuration files.

The `represent` user's directory contains:

* `app/`: a clone of [represent-canada](https://github.com/opennorth/represent-canada/)
* `app/represent/settings.py`: a copy of `settings.py.example` with appropriate changes
* `app/data/shapefiles/public`: a symlink to a clone of `represent-canada-data`
* `app/data/shapefiles/private`: a symlink to a clone of `represent-canada-private-data`
* `logs/`: Gunicorn and Nginx log files
* `ssl/`: public key certificates
* a clone of [represent-canada-data](https://github.com/opennorth/represent-canada-data/)
* a clone of `represent-canada-private-data`
* `represent-env/`: a Python 3.5 virtualenv

The `represent` user's crontab contains:

```
MAILTO=represent@opennorth.ca
0 4 * * * /home/represent/.virtualenvs/app35/bin/python /home/represent/app/manage.py updaterepresentatives
```

### Adding a maintainer

Add the maintainer's public key to `represent`'s `.ssh/authorized_keys` on `alpheus` and `tempeh`

### Running Fabric commands

It's generally unnecessary to login to servers, as regular tasks can be done with Fabric. See `fabfile.py` for details.

    brew install Fabric

The two most common tasks are to deploy code and update boundaries.

Run `fab alpheus deploy` to update the deployment; occasionally, update the deployment on `tempeh` (`fab tempeh deploy`).

Run `fab alpheus update_boundaries` to update the boundaries. You can pass arguments like:

    fab alpheus update_boundaries:args="--merge union -d data/shapefiles/public/boundaries/ocd-division/country:ca/2013"

## DNS

`opennorth.ca` has a hosted zone and health check in [AWS Route 53](https://console.aws.amazon.com/route53/home?region=us-east-1#). Notably:

* `represent-alpheus.opennorth.ca.` aliases `alpheus.opennorth.ca.`
* `represent-tempeh.opennorth.ca.` aliases `tempeh.opennorth.ca.`
* `represent.opennorth.ca.` aliases `represent-alpheus.opennorth.ca.`
  * TTL: 60, Routing Policy: Failover, Failover Record Type: Primary
* `represent.opennorth.ca.` aliases `represent-tempeh.opennorth.ca.`
  * TTL: 60, Routing Policy: Failover, Failover Record Type: Secondary

A health check named `represent-alpheus.opennorth.ca` monitors an endpoint specified by domain name using the HTTP protocol. The domain name is `represent-alpheus.opennorth.ca` and the port is `80`.

# Deployment

## Servers

Two dedicated servers from [server4you.com](https://www.server4you.com/), `ohoh` and `tofu`, host [represent.opennorth.ca](https://represent.opennorth.ca/) and [openparliament.ca](https://openparliament.ca/). The servers are identical, except there is PostgreSQL master-slave replication between `ohoh` and `tofu`. If `ohoh` goes down, Represent fails over to `tofu` ([see below](#dns)). The servers run Nginx, PostGIS and Memcached.

This directory contains some server configuration files.

The `represent` user's directory contains:

* `app/`: a clone of [represent-canada](https://github.com/opennorth/represent-canada/)
* `app/represent/settings.py`: a copy of `settings.py.example` with appropriate changes
* `app/data/shapefiles/public`: a symlink to a clone of `represent-canada-data`
* `app/data/shapefiles/private`: a symlink to a clone of `represent-canada-data-private`
* `logs/`: Gunicorn and Nginx log files
* `ssl/`: public key certificates
* a clone of [represent-canada-data](https://github.com/opennorth/represent-canada-data/)
* a clone of `represent-canada-data-private`
* `.virtualenvs/app35`: a Python 3.5 virtualenv

The `represent` user's crontab contains:

```
MAILTO=represent@opennorth.ca
0 4 * * * /home/represent/.virtualenvs/app35/bin/python /home/represent/app/manage.py updaterepresentatives
```

### Adding a maintainer

Add the maintainer's public key to `represent`'s `.ssh/authorized_keys` on `ohoh` and `tofu`

### Running Fabric commands

It's generally unnecessary to login to servers, as regular tasks can be done with Fabric. See `fabfile.py` for details.

    pip install Fabric

The two most common tasks are to deploy code and update boundaries.

Run `fab ohoh deploy` to update the deployment; occasionally, update the deployment on `tofu` (`fab tofu deploy`).

Run `fab ohoh update_boundaries` to update the boundaries. You can pass arguments like:

    fab ohoh update_boundaries:args="--merge union -d data/shapefiles/public/boundaries/ocd-division/country:ca/2013"

## DNS

`opennorth.ca` has a hosted zone and health check in [AWS Route 53](https://console.aws.amazon.com/route53/home?region=us-east-1#). Notably:

* `represent-ohoh.opennorth.ca.` CNAME `ohoh.openparliament.ca.` TTL: 1800
* `represent-tofu.opennorth.ca.` CNAME `tofu.michaelmulley.com.` TTL: 1800
* `represent.opennorth.ca.` CNAME `ohoh.openparliament.ca.` TTL: 60, Routing Policy: Failover, Failover Record Type: Primary
* `represent.opennorth.ca.` CNAME `tofu.openparliament.ca.` TTL: 60, Routing Policy: Failover, Failover Record Type: Secondary

A health check named `represent-ohoh.opennorth.ca` monitors an endpoint specified by domain name using the HTTP protocol. The domain name is `represent-ohoh.opennorth.ca` and the port is `80`.

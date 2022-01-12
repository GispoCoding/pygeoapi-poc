# pygeoapi-poc

This repository contains a sample [pygeoapi](https://pygeoapi.io/) deployment with a PostGIS backend.
Main pygeoapi configuration is located in [pygeoapi-config.yml](pygeoapi-config.yml).

Custom processes are placed in the `custom_process` directory that gets mounted inside the pygeoapi container.
The directory contains four example processes that can be used via the OGC Processes API provided by pygeoapi.
See [requests.sh](requests.sh) for usage examples.

## Dependencies

All services run inside Docker containers.
Docker Compose files are provided for ease of use.
Make sure you have `docker` and `docker-compose` installed.

The `load_data.sh` script depends on `wget`, `unzip`, `ogr2ogr` and `gdalwarp`.
The script will warn you if these commands are not found in PATH, install them as necessary.

## Running locally

Configure PostGIS and GeoServer passwords using the example .env file: `cp .env.example .env && vim .env`.

Set up the PostGIS database: `./load_data.sh && docker-compose -f docker-compose.db.yaml up -d`.
**Note**: the `data/jarvi10.sql` file is imported every time the database is restarted.
Restarting the DB can take up to a few minutes, check progress by running `docker-compose -f docker-compose.db.yaml logs --follow`.

Run pygeoapi: `docker-compose up -d`.
Open [localhost:5000](http://localhost:5000) in your web browser.
**Note**: if you run into problems, check the pygeoapi log with `docker-compose logs`.

Run GeoServer and nginx (optional): `docker-compose -f docker-compose.gs.yaml up -d && sleep 30 && docker-compose -f docker-compose.nginx.yaml up -d`.
You can now access pygeoapi at [localhost](http://localhost/) and GeoServer at [localhost/geoserver](http://localhost/geoserver/).

## Teardown

Stop all running services by running: `docker-compose down --remove-orphans`.

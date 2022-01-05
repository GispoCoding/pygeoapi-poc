#!/usr/bin/env bash

set -e

mkdir -p data
cd data

wget https://wwwd3.ymparisto.fi/d3/gis_data/spesific/ranta10jarvet.zip && unzip ranta10jarvet.zip
ogr2ogr --config PG_USE_COPY YES -f PGDump jarvi10.sql jarvi10.shp -lco SRID=3067 -lco PRECISION=NO

wget https://wwwd3.ymparisto.fi/d3/Static_rs/spesific/clc2018_fi20m.zip && unzip clc2018_fi20m.zip

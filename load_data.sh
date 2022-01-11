#!/usr/bin/env bash

set -e

if [ -d "data" ]; then
  echo 'Error: data directory already exists'
  exit 1
fi

if ! command -v wget &> /dev/null; then
  echo 'Error: command wget not in PATH'
  exit 1
fi

if ! command -v unzip &> /dev/null; then
  echo 'Error: command unzip not in PATH'
  exit 1
fi

if ! command -v ogr2ogr &> /dev/null; then
  echo 'Error: command ogr2ogr not in PATH'
  exit 1
fi

if ! command -v gdalwarp &> /dev/null; then
  echo 'Error: command gdalwarp not in PATH'
  exit 1
fi

mkdir -p data
cd data

wget https://wwwd3.ymparisto.fi/d3/gis_data/spesific/ranta10jarvet.zip && unzip ranta10jarvet.zip

ogr2ogr --config PG_USE_COPY YES -f PGDump jarvi10.sql jarvi10.shp -a_srs EPSG:3067 -t_srs EPSG:4326 -lco GEOMETRY_NAME=wgs_geom -lco PRECISION=NO

wget https://wwwd3.ymparisto.fi/d3/Static_rs/spesific/clc2018_fi20m.zip && unzip clc2018_fi20m.zip

gdalwarp -te 389000 7216000 390000 7217000 Clc2018_FI20m.tif miniclc.tif

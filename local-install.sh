#!/usr/bin/env bash

# Set up and run pygeoapi in a Python venv on Ubuntu 20.04

sudo apt install python3-venv
git clone https://github.com/geopython/pygeoapi.git pygeoapi-poc
cd pygeoapi-poc
git checkout 0.11.0

python3 -m venv .venv
source .venv/bin/activate
pip install wheel && pip install pygeoapi

pygeoapi openapi generate pygeoapi-config.yml > openapi.yml
pygeoapi openapi validate openapi.yml
export PYGEOAPI_CONFIG=$(pwd)/pygeoapi-config.yml
export PYGEOAPI_OPENAPI=$(pwd)/openapi.yml

pygeoapi serve
# for production use, see https://docs.pygeoapi.io/en/stable/running.html#running-in-production

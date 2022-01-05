import logging
import os

import psycopg2

from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError


LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '1.0.0',
    'id': 'reproj',
    'title': {
        'en': 'Reproject Linestring',
    },
    'description': {
        'en': 'Reprojects a Linestring to another CRS.'
    },
    'keywords': ['reproject', 'line', 'geometry'],
    'links': [{
        'type': 'text/html',
        'rel': 'canonical',
        'title': 'information',
        'href': 'https://syke.fi/',
        'hreflang': 'fi-FI'
    }],
    'inputs': {
        'geom': {
            'title': 'Geometry',
            'description': 'The geometry you want to reproject in Linestring WKT format.',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['geometry']
        },
        'in_crs': {
            'title': 'Input CRS',
            'description': 'The EPSG ID number of the input geometry.',
            'schema': {
                'type': 'number'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['crs srs']
        },
        'out_crs': {
            'title': 'Output CRS',
            'description': 'The EPSG ID number of the CRS you want to reproject to.',
            'schema': {
                'type': 'number'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['crs srs']
        },
    },
    'outputs': {
        'reprojected_geometry': {
            'title': 'Reprojected geometry',
            'description': 'A JSON document containing reprojected geometry in Linestring WKT format',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'geom': '',
            'in_crs': 4326,
            'out_crs': 3067
        }
    }
}


class ReprojProcessor(BaseProcessor):
    """Exterior Processor"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.custom_process.reproj.ReprojProcessor
        """

        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data):

        mimetype = 'application/json'
        in_crs = data.get('in_crs', None)
        out_crs = data.get('out_crs', None)
        geom = data.get('geom', None)

        if not all((in_crs, out_crs, geom)):
            raise ProcessorExecuteError('Missing some parameters')

        pgpass = os.environ["POSTGRES_PASS"]
        conn = psycopg2.connect(user="postgres", password=pgpass, host="pygeoapi-poc_postgis_1", port="5432", database="gis")

        cur = conn.cursor()
        query = "SELECT ST_AsText(ST_Transform(ST_GeomFromText(%s, %s), %s))"
        cur.execute(query, (geom, in_crs, out_crs,))

        result = cur.fetchone()
        conn.close()

        if not result:
            raise ProcessorExecuteError("No output geometry generated")
        elif len(result) != 1:
            raise ProcessorExecuteError("Invalid result from database")

        outputs = {
            'reprojected_geometry': result[0]
        }

        return mimetype, outputs

    def __repr__(self):
        return '<ExtProcessor> {}'.format(self.name)

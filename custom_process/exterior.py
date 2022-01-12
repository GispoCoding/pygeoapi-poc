import logging
import os

import psycopg2

from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError


LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '1.0.0',
    'id': 'exterior',
    'title': {
        'en': 'Lake exterior ring',
    },
    'description': {
        'en': 'Returns the exterior ring of a lake matching the given name.'
    },
    'keywords': ['exterior', 'lake', 'geometry'],
    'links': [{
        'type': 'text/html',
        'rel': 'canonical',
        'title': 'information',
        'href': 'https://syke.fi/',
        'hreflang': 'fi-FI'
    }],
    'inputs': {
        'name': {
            'title': 'Name',
            'description': 'The name of the lake you want to get the exterior ring of.',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['lake name']
        },
    },
    'outputs': {
        'ext_ring': {
            'title': 'Exterior ring',
            'description': 'A JSON document containing the OGC FID of the matched lake, its name, '
            'and the exterior ring geometry in Linestring WKT format',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'name': 'Haukkalampi'
        }
    }
}


class ExtProcessor(BaseProcessor):
    """Exterior Processor"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.custom_process.exterior.ExtProcessor
        """

        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data):

        mimetype = 'application/json'
        name = data.get('name', None)

        if name is None:
            raise ProcessorExecuteError('Cannot process without a name')

        pghost = os.environ["DB_HOSTNAME"]
        pgpass = os.environ["POSTGRES_PASS"]
        conn = psycopg2.connect(user="postgres", password=pgpass, host=pghost, port="5432", database="gis")

        cur = conn.cursor()
        query = "SELECT ogc_fid, nimi, ST_AsText(ST_ExteriorRing(wgs_geom)) AS ext_ring FROM public.jarvi10 WHERE nimi = %s LIMIT 1;"
        cur.execute(query, (name,))

        result = cur.fetchone()
        conn.close()

        if not result:
            raise ProcessorExecuteError(f"No lake found with name {name}")
        elif len(result) != 3:
            raise ProcessorExecuteError("Invalid result from database")

        outputs = {
            'ogc_fid': result[0],
            'name': result[1],
            'ext_geom_wkb': result[2]
        }

        return mimetype, outputs

    def __repr__(self):
        return '<ExtProcessor> {}'.format(self.name)

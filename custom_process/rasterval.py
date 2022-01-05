import logging

import rasterio as rio

from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError


LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '1.0.0',
    'id': 'rasterval',
    'title': {
        'en': 'CORINE raster value picker',
    },
    'description': {
        'en': 'Returns the value of the CORINE land cover raster at the given location.'
    },
    'keywords': ['raster', 'value', 'corine'],
    'links': [{
        'type': 'text/html',
        'rel': 'canonical',
        'title': 'information',
        'href': 'https://syke.fi/',
        'hreflang': 'fi-FI'
    }],
    'inputs': {
        'x': {
            'title': 'X coordinate',
            'description': 'X coordinate in EPSG:3067 ',
            'schema': {
                'type': 'number'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['x coordinate']
        },
        'y': {
            'title': 'Y coordinate',
            'description': 'Y coordinate in EPSG:3067 ',
            'schema': {
                'type': 'number'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['x coordinate']
        },
    },
    'outputs': {
        'raster_value': {
            'title': 'CORINE raster value',
            'description': 'Value of the CORINE landcover raster at the given location',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'x': 389500,
            'y': 7216500
        }
    }
}


class ValProcessor(BaseProcessor):
    """Exterior Processor"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.custom_process.rasterval.ValProcessor
        """

        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data):

        mimetype = 'application/json'
        x = data.get('x', None)
        y = data.get('y', None)

        if x is None or y is None:
            raise ProcessorExecuteError('Cannot process X or Y coordinates')

        with rio.open("/data/Clc2018_FI20m.tif") as dataset:
            value = int([v[0] for v in dataset.sample([(x, y)])][0])

        outputs = {
            'raster_value': value,
        }

        return mimetype, outputs

    def __repr__(self):
        return '<ExtProcessor> {}'.format(self.name)

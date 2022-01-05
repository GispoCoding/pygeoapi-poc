import logging

from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError


LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '1.0.0',
    'id': 'hello2',
    'title': {
        'en': 'Custom helloworld',
        'fr': 'Bonjour'
    },
    'description': {
        'en': 'A customised example process that takes a name as input, and echoes '
              'it back as output. Intended to demonstrate a simple '
              'process with a single literal input.',
        'fr': 'Un exemple de processus qui prend un nom en entrée et le '
              'renvoie en sortie. Destiné à démontrer un processus '
              'simple avec une seule entrée littérale.',
    },
    'keywords': ['customhelloworld', 'test example', 'echo'],
    'links': [{
        'type': 'text/html',
        'rel': 'canonical',
        'title': 'information',
        'href': 'https://gispo.fi/',
        'hreflang': 'fi-FI'
    }],
    'inputs': {
        'name': {
            'title': 'Name',
            'description': 'The name of the person or entity that you wish to'
                           'be echoed back as an output',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['full name', 'personal']
        },
        'message': {
            'title': 'Message',
            'description': 'An optional message to echo as well',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'metadata': None,
            'keywords': ['message']
        }
    },
    'outputs': {
        'echo': {
            'title': 'World',
            'description': 'A "world" echo with the name and (optional)'
                           ' message submitted for processing',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'name': 'World',
            'message': 'An optional message.',
        }
    }
}


class WorldProcessor(BaseProcessor):
    """World Processor example"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.custom_process.world.WorldProcessor
        """

        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data):

        mimetype = 'application/json'
        name = data.get('name', None)

        if name is None:
            raise ProcessorExecuteError('Cannot process without a name')

        value = 'Customised helloes {}! {}'.format(name, data.get('message', '')).strip()

        outputs = {
            'id': 'echo',
            'value': value
        }

        return mimetype, outputs

    def __repr__(self):
        return '<WorldProcessor> {}'.format(self.name)

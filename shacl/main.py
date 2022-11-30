import sys

import rdflib

# os.environ['http_proxy'] = 'http://localhost:3128'
# os.environ['https_proxy'] = 'http://localhost:3128'
# os.environ["REQUESTS_CA_BUNDLE"] = '/usr/local/share/ca-certificates/myCA.pem'
# os.environ["SSL_CERT_FILE"] = '/usr/local/share/ca-certificates/myCA.pem'
from shacl.constants import BASE_DIR, MODE
from shacl.log.log import register_logger
from shacl.validate import ValidationRun

# Where are the files living

# SHACL rules

# The data to be validated (In this case the postdam dataset)
# DATA_URL = 'datenadler.ttl'
DATA_URL = 'first_1000.ttl'

print('Parsing Input')
graph_file = BASE_DIR / 'data' / DATA_URL

register_logger()

# todo: Replace paths by database
validation = ValidationRun(graph_file, BASE_DIR / 'results' / 'validated_output.ttl', BASE_DIR / 'results' / 'report_graph{steps}.ttl')

validation.run(mode=MODE)

sys.exit(0)

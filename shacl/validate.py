import sys
from pathlib import Path

import pyshacl

# Where are the files living
BASE_DIR = Path('/home/volker/workspace/PYTHON5/SHACL_validation')

# SHACL rules
SHAPE_FILES = [
    'dcat-ap_2.1.1_shacl_shapes.ttl',
    'dcat-ap-spec-german-additions.ttl',
    'dcat-ap-spec-german-messages.ttl',
]

# The data to be validated (In this case the postdam dataset)
DATA_URL = 'first_1000.ttl'

# Import the SHACL rules

validator = pyshacl.rdfutil.load_from_source(str(BASE_DIR / 'shapes' / SHAPE_FILES[0]))

if len(SHAPE_FILES) > 1:
    for filename in SHAPE_FILES[1:]:
        validator = pyshacl.rdfutil.load_from_source(str(BASE_DIR / 'shapes' / filename), g=validator)


graph_data = open(BASE_DIR / 'data' / DATA_URL, 'rb')


conforms, report_graph, report_text = pyshacl.validate(
    data_graph=graph_data,
    shacl_graph=validator,
    ont_graph=str(BASE_DIR / 'shapes' / 'dcat-ap-de-imports.ttl'),
    do_owl_imports=True,
    ont_graph_format='turtle',
    data_graph_format='turtle',
    meta_shacl= False,
)

print(report_text)

sys.exit(0)

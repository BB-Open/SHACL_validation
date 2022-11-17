import sys
from pathlib import Path

import kglab
import pyshacl
import rdflib

# Where are the files living
BASE_DIR = Path('/home/volker/workspace/PYTHON5/SHACL_validation')

# Data files
DCAT_FILES = [
#    'nal-lists.ttl',
]

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
    meta_shacl= True,
)

print(report_text)

sys.exit(0)

sparql = """
SELECT DISTINCT ?severity ?focus ?path ?value ?message
  WHERE {
    VALUES (?severity ?severity_idx) { 
        (sh:Violation  0)
        (sh:Warning 1)
        (sh:Info 2)
    }
    bind("<nicht vorhanden>" as ?default_value)
    
    ?id a sh:ValidationResult .
    ?id sh:resultSeverity ?severity .
    ?id sh:focusNode ?focus .
    ?id sh:resultPath ?path .
    ?id sh:resultMessage ?message .
    OPTIONAL {
        ?id sh:value ?value .
    }
    
    bind(coalesce(?value, ?default_value) as ?value)
  }
  ORDER BY ?severity_idx ?focus ?path 
"""
#sparql = """SELECT ?s ?o ?p WHERE {?s ?o ?p} ORDER BY ?s"""


report_graph.use_gpus = False



pyvis_graph = kglab.SubgraphTensor(report_graph).build_pyvis_graph(notebook=True)
pyvis_graph.show_buttons()
pyvis_graph.force_atlas_2based()
pyvis_graph.show("result_graph.html")



df = report_graph.query_as_df(sparql)
df.to_html('table.html')

import kglab
from os.path import join
import pandas as pd
#pd.set_option("max_rows", None)


# Where are the files living
BASE_DIR = '/home/volker/workspace/PYTHON2/shacl/shapes'

# Data files
DCAT_FILES = [
    'dcat-ap-de-imports.ttl',
    'dcat-ap-spec-german-additions.ttl',
    'dcat-ap-spec-german-messages.ttl',
    'dcat-ap_2.1.1_shacl_shapes.ttl',
#    'nal-lists.ttl',
]

# SHACL rules
SHAPE_FILES = [
]

# The data to be validated (In this case the postdam dataset)
# DATA_URL = 'https://opendata.potsdam.de/api/v2/catalog/exports/ttl?limit=1'
# DATA_URL = 'https://flask.datenadler.de/download'
DATA_URL = 'file:///home/volker/workspace/PYTHON2/shacl/data/first_1000.ttl'


validator = kglab.KnowledgeGraph(
    name = "A DCAT-AP.de validator",
    base_uri = "https://dcat.validator",
    use_gpus =False,
    )

# Import the DCAT files
for filename in DCAT_FILES:
    validator.load_rdf(join(BASE_DIR, filename),format='turtle')

# Import the SHACL rules
for filename in SHAPE_FILES:
    validator.load_rdf(join(BASE_DIR, filename), format='turtle')


data = kglab.KnowledgeGraph(
    name = "Potsdam Data",
    base_uri = "https://potsdam",
    use_gpus =False,
    )


data.load_rdf(DATA_URL, format='turtle')

conforms, report_graph, report_text = data.validate(shacl_graph=validator.rdf_graph())

print(report_text)

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

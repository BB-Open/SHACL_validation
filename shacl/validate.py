import sys
from pathlib import Path

import pyshacl

import os

import rdflib
from rdflib import URIRef, Namespace

from shacl.timeit import catchtime, timeit

# os.environ['http_proxy'] = 'http://localhost:3128'
# os.environ['https_proxy'] = 'http://localhost:3128'
# os.environ["REQUESTS_CA_BUNDLE"] = '/usr/local/share/ca-certificates/myCA.pem'
# os.environ["SSL_CERT_FILE"] = '/usr/local/share/ca-certificates/myCA.pem'

REMOVE_SPARQL = """
PREFIX sh: <http://www.w3.org/ns/shacl#>
prefix dct: <http://purl.org/dc/terms/>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix dcat: <http://www.w3.org/ns/dcat#>
prefix dcatde: <http://dcat-ap.de/def/dcatde/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix adms: <http://www.w3.org/ns/adms#>
prefix owl: <http://www.w3.org/2002/07/owl>
prefix schema: <http://schema.org/>
prefix spdx: <http://spdx.org/rdf/terms#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix vcard: <http://www.w3.org/2006/vcard/ns#>
prefix rdf4j: <http://rdf4j.org/schema/rdf4j#>
prefix sesame: <http://www.openrdf.org/schema/sesame#>
prefix fn: <http://www.w3.org/2005/xpath-functions#>

DELETE {
    ?node ?path ?value
}
WHERE
{
    ?res a sh:ValidationResult ;
        sh:focusNode ?node ;
        sh:resultPath ?path ;
        sh:value ?value .
}
"""

SHACL_RESULTS = """
PREFIX sh: <http://www.w3.org/ns/shacl#>

SELECT ?node ?path ?value ?severity
WHERE
{
    ?res a sh:ValidationResult ;
        sh:resultSeverity ?severity ;
        sh:focusNode ?node ;
        sh:resultPath ?path ;
        OPTIONAL {
           ?res sh:value ?value ;
        } .
}
"""

NUMBER_OF_DATASETS = """
PREFIX dcat:   <http://www.w3.org/ns/dcat#>
PREFIX dcatap: <http://data.europa.eu/r5r#>
PREFIX dcatde: <http://dcat-ap.de/def/dcatde/>

SELECT (COUNT(?s) AS ?count)
 
WHERE
{{
    {}
}}
"""

# Where are the files living
BASE_DIR = Path('/home/sandra/workspace/SHACL_validation')

# SHACL rules
SHAPE_FILES = [
    'dcat-ap_2.1.1_shacl_shapes.ttl',
#    'dcat-ap-spec-german-additions.ttl',
#    'dcat-ap-spec-german-messages.ttl',
]

# The data to be validated (In this case the postdam dataset)
DATA_URL = 'first_1000.ttl'
# DATA_URL = 'datenadler.ttl'


def statistic( stage, graph ):
    print(stage)
    a = graph.query(NUMBER_OF_DATASETS.format('?s a dcat:Dataset'))
    print('datasets: ', a.bindings[0]['count'])
    a = graph.query(NUMBER_OF_DATASETS.format('?s a dcat:Distribution'))
    print('distributions: ', a.bindings[0]['count'])
    a = graph.query(NUMBER_OF_DATASETS.format('?s ?p ?o'))
    print('nodes:', a.bindings[0]['count'])


class Validator:
    """Validator instance"""

    def __init__(self):
        self.first_run = True
        # Import the SHACL rules
        self.validator = pyshacl.rdfutil.load_from_source(str(BASE_DIR / 'shapes' / SHAPE_FILES[0]))

        if len(SHAPE_FILES) > 1:
            for filename in SHAPE_FILES[1:]:
                self.validator = pyshacl.rdfutil.load_from_source(str(BASE_DIR / 'shapes' / filename), g=self.validator)

        self.ont_graph = rdflib.graph.Graph()
        self.ont_graph.parse(str(BASE_DIR / 'shapes' / 'dcat-ap-de-imports.ttl'))

    def validate(self, graph_data):

        if self.first_run :
            conforms, report_graph, report_text = pyshacl.validate(
                data_graph=graph_data,
                shacl_graph=self.validator,
                ont_graph=self.ont_graph,
                do_owl_imports=True,
                meta_shacl=False,
            )
        else:
            conforms, report_graph, report_text = pyshacl.validate(
                data_graph=graph_data,
                shacl_graph=self.validator,
                do_owl_imports=True,
                meta_shacl=False,
            )
        self.first_run = False
        return conforms, report_graph, report_text

print("Creating validator")
validator = Validator()

graph = rdflib.graph.Graph()
print('Parsing Input')
graph_data = graph.parse(open(BASE_DIR / 'data' / DATA_URL, 'rb'))

data_conforms = False
steps = 1

SH = Namespace('http://www.w3.org/ns/shacl#')

while not data_conforms:
    print("validating")
    conforms, report_graph, report_text = validator.validate(graph_data)

    report_graph.serialize(BASE_DIR / 'results' / f'report_graph{steps}.ttl', 'turtle')

    print(f'\nstep: {steps}')
    steps += 1

    statistic('\nInput Data: ', graph_data)

    print('\nViolations: ', len([i for i in report_graph.triples((None, None, URIRef('http://www.w3.org/ns/shacl#ValidationResult')))]))

    print(report_text)

    shacl_results = report_graph.query(SHACL_RESULTS)

    data_conforms = True
    for shacl_result in shacl_results.bindings:
        if 'severity' in shacl_result:
            sev = shacl_result['severity']
            if sev == SH.Violation:
                # something will be removed, check again with the rest
                data_conforms = False
                if 'value' in shacl_result:
                    graph_data.remove((shacl_result['node'], shacl_result['path'], shacl_result['value']))
                else:
                    graph_data.remove((shacl_result['node'], None, None))
                    graph_data.remove((None, shacl_result['node'], None))
                    graph_data.remove((None, None, shacl_result['node']))
            else:
                print(sev)
                print('No Violation')
        else:
            print('No severity')

    graph_data.commit()

    statistic('\nValidated Data', graph_data)


graph_data.serialize(BASE_DIR / 'results' / 'validated_output.ttl', 'turtle')

sys.exit(0)

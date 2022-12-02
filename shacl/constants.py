import os
from pathlib import Path

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

SELECT ?node ?path ?value ?severity ?msg ?sourceConstraintComponent ?sourceShape
WHERE
{
    ?res a sh:ValidationResult ;
        sh:resultSeverity ?severity ;
        sh:focusNode ?node ;
        sh:resultPath ?path ;
        sh:sourceConstraintComponent ?sourceConstraintComponent;
        sh:sourceShape ?sourceShape;
        OPTIONAL {
           ?res sh:value ?value ;
        } .
        OPTIONAL {
           ?res sh:resultMessage ?msg ;
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
BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__))) / '..'
SHAPE_FILES = [
    'dcat-ap_2.1.1_shacl_shapes.ttl',
#    'dcat-ap-spec-german-additions.ttl',
#    'dcat-ap-spec-german-messages.ttl',
]
QUERY_ALL = '''
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
CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o }
'''
TABLE_HEADER = """
<table>
  <tr>
    <th>Severity</th>
    <th>#</th>
    <th>Message</th>
    <th>sourceConstraintComponent</th>
    <th>sourceShape</th>
    <th>Node</th>
    <th>Path</th>
    <th>Value</th>
  </tr>
"""
HTML_STYLE = """
            <style>
table, th, td, div {
  border: 1px solid;
  margin: 5px;
  padding: 5px;
}
</style>
            """
PDF_STYLE = """
@page { 
    size: A4 landscape; 
    margin: 1cm;
}

body {
    font-size: 0.7em;
}

table, th, td, div {
    border: 1px solid;
    margin: 5px;
    padding: 5px;
}
table {
    table-layout: fixed;
    width: 27cm;
    overflow-wrap: break-word
}
tr, div {
    page-break-inside: avoid;
}

"""
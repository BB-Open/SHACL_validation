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
NUMBER_OF_QUERY = """
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
SHAPE_FILES_META = {
    'dcat-ap_2.1.1_shacl_shapes.ttl': {
        'version': '2.1.1',
        'last_download': '2023-03-07',
        'last_change': '2022-08-12',
        'notes': 'xsd:dateTimeStamp als Datumstyp ergänzt',
    },
    'dcat-ap-spec-german-additions.ttl': {
        'version': 'v2.0',
        'last_download': '2023-03-07',
        'last_change': '2023-01-23',
        'notes': '',
    },
    'dcat-ap-spec-german-messages.ttl': {
        'version': 'v2.0',
        'last_download': '2023-03-07',
        'last_change': '2022-08-18',
        'notes': '',
    },
    'dcat-ap-de-imports.ttl': {
        'version': 'v2.0',
        'last_download': '2023-03-07',
        'last_change': '2023-01-02',
        'notes': '',
    },
}

SHAPE_FILES = [
    'dcat-ap_2.1.1_shacl_shapes.ttl',
    'dcat-ap-spec-german-additions.ttl',
    'dcat-ap-spec-german-messages.ttl',
    'dcat-ap-de-imports.ttl',
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
    <th>Meldung</th>
    <th>Fälle</th>
    <th>Nachricht</th>
    <th>Regel</th>
    <th>Bedingung</th>
    <th>Knoten</th>
    <th>Pfad</th>
    <th>Wert</th>
  </tr>
"""

HTML_STYLE = """
table, th, td, div {

}

table, th, td, div {
  border: 1px solid black;
  border-collapse: collapse;
}

th, td, div {
    padding: 5px;
}

table, div {
    margin: 5px;
}

h3, h4 {
    margin-top: 12px;
    margin-bottom: 5px;
}

 ul,  p {
    margin-top: 5px;
    margin-bottom: 5px;
}
h3, h4, p {
    padding: 0
}

"""
TABLE_PDF_STYLE = """
@page { 
    size: A4 landscape; 
    margin: 1cm;
}

table {
    width: 27cm;
}
"""

BLOCKS_PDF_STYLE = """
@page { 
    size: A4; 
    margin: 1cm;
}

table {
    width: 18.3cm;
}
"""

PDF_STYLE = HTML_STYLE + """

body {
    font-size: 0.7em;
}

table {
    table-layout: fixed;
    overflow-wrap: break-word
}
tr, div {
    page-break-inside: avoid;
}

"""
COLORS = {
    'Fehler': '#ffe6e6',
    'Warnung': '#ffeecc',
    'Info': '#f2ffcc',
}
SEVS = ['Fehler', 'Warnung', 'Info']

COMPARISON_TABLE_HEADER = """
<table>
  <tr>
    <th></th>
    <th>Anzahl vor der Validierung</th>
    <th>Anzahl nach der Validierung</th>
  </tr>
"""

SHACL_FILES_TABLE_HEADER = """
<table>
  <tr>
    <th>Datei</th>
    <th>Version</th>
    <th>Letzte Aktualisierung im Repository</th>
    <th>Letzter Download</th>
    <th>Anmerkungen</th>
  </tr>
"""

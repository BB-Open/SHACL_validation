import sys
from datetime import datetime

from pkan_config.config import get_config
from pyrdf4j.errors import QueryFailed
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth

from shacl.constants import BASE_DIR, NUMBER_OF_QUERY
from shacl.log.log import get_logger
from shacl.report import HTMLTableReport, PDFTableReport, HTMLBlockReport, PDFBlockReport
from shacl.shacl_db import fill_shacl_db
from shacl.validate import ValidationRun

input_data = 'complete_store'
output = 'complete_store_validate'
output_error = 'complete_store_error'

# input_data = BASE_DIR / 'data' / 'datenadler.ttl'
# input_data = BASE_DIR / 'data' / 'first_1000.ttl'
# output = BASE_DIR / 'results' / 'validated_output.ttl'
# output_error = BASE_DIR / 'results' / 'report_graph.ttl'

pdf_file = BASE_DIR / 'results' / 'report_rdf4j_table.pdf'
html_file = BASE_DIR / 'results' / 'report_rdf4j_table.html'
pdf_file2 = BASE_DIR / 'results' / 'report_rdf4j.pdf'
html_file2 = BASE_DIR / 'results' / 'report_rdf4j.html'

logger = get_logger()

logger.info('Starting Validation Process')

logger.info('FILL SHACL STORES')

# this will be done once on scheduler start
fill_shacl_db()

logger.info('VALIDATE INFORMATION')

validation = ValidationRun(input_data, output, output_error)
#
validation.run()

logger.info('GENERATE REPORTS')

# just one report needed in live system

# collect some additional data
COMPARISON_FIELDS = {
    'Triple Gesamt': '?s ?p ?o',
    'Kataloge': '?s a dcat:Catalog',
    'Datensätze': '?s a dcat:Dataset',
    'Distributionen': '?s a dcat:Distribution'
}

cfg = get_config()
comparison_fields = []
if cfg.SHACL_MODE == 'store':
    rdf4j = RDF4J(rdf4j_base=cfg.RDF4J_BASE)
    auth = HTTPBasicAuth(cfg.ADMIN_USER, cfg.ADMIN_PASS)

    for field, short_query in COMPARISON_FIELDS.items():
        query = NUMBER_OF_QUERY.format(short_query)
        try:
            old = rdf4j.query_repository(input_data, query=query, auth=auth)
            new = rdf4j.query_repository(output, query=query, auth=auth)
        except QueryFailed:
            continue
        comparison_fields.append({
            'field': field,
            'old': old['results']['bindings'][0]['count']['value'],
            'new': new['results']['bindings'][0]['count']['value']
        })

provider = 'Unbekannt'
date = datetime.now()
date_formatted = date.strftime('%Y-%m-%d %H:%M')

# reports will be generated on demand, so stores are reloaded
HTMLTableReport().generate(output_error, html_file, display_details=True, provider=provider,
                           date=date_formatted, comparison_fields=comparison_fields)
PDFTableReport().generate(output_error, pdf_file, display_details=True, provider=provider,
                          date=date_formatted, comparison_fields=comparison_fields)
HTMLBlockReport().generate(output_error, html_file2, display_details=True, provider=provider,
                           date=date_formatted, comparison_fields=comparison_fields)
PDFBlockReport().generate(output_error, pdf_file2, display_details=True, provider=provider,
                          date=date_formatted, comparison_fields=comparison_fields)

sys.exit(0)

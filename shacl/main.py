import sys

import rdflib

# os.environ['http_proxy'] = 'http://localhost:3128'
# os.environ['https_proxy'] = 'http://localhost:3128'
# os.environ["REQUESTS_CA_BUNDLE"] = '/usr/local/share/ca-certificates/myCA.pem'
# os.environ["SSL_CERT_FILE"] = '/usr/local/share/ca-certificates/myCA.pem'
from shacl.constants import BASE_DIR
from shacl.log.log import get_logger
from shacl.report import HTMLTableReport, PDFTableReport, HTMLBlockReport, PDFBlockReport
from shacl.validate import ValidationRun

# Where are the files living

# SHACL rules

print('Parsing Input')

get_logger()

input_data = 'potsdam_complete'
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

validation = ValidationRun(input_data, output, output_error)
#
validation.run()

# just one report needed in live system
# reports will be generated on demand, so stores are reloaded
HTMLTableReport().generate(output_error, html_file, display_details=True)
PDFTableReport().generate(output_error, pdf_file, display_details=True)
HTMLBlockReport().generate(output_error, html_file2, display_details=True)
PDFBlockReport().generate(output_error, pdf_file2, display_details=True)

sys.exit(0)

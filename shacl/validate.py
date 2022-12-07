import pyshacl
import rdflib
from pkan_config.config import get_config
from pyrdf4j.rdf4j import RDF4J
from rdflib import URIRef
from requests.auth import HTTPBasicAuth
from zope import component

from shacl.constants import NUMBER_OF_QUERY, SHACL_RESULTS
from shacl.log.log import ILogger
from shacl.namespaces import SH
from shacl.preprocess import Preprocess
from shacl.results import ResultWriter


class Validator:
    """Validator instance"""

    def __init__(self, mode, auth, rdf4j):
        self.first_run = True
        # Import the SHACL rules

        prep = Preprocess(mode=mode, auth=auth, rdf4j=rdf4j)

        self.validator, self.ont_graph = prep.load_shacl()

    def validate(self, input):

        if self.first_run :
            conforms, report_graph, report_text = pyshacl.validate(
                data_graph=input,
                shacl_graph=self.validator,
                ont_graph=self.ont_graph,
                do_owl_imports=True,
                meta_shacl=False,
            )
        else:
            conforms, report_graph, report_text = pyshacl.validate(
                data_graph=input,
                shacl_graph=self.validator,
                do_owl_imports=True,
                meta_shacl=False,
            )
        self.first_run = False
        return conforms, report_graph, report_text


class ValidationRun:
    """
    Handle one Run
    """

    def __init__(self, input_file, output_file, output_error_file, visitor=None):
        self.logger = component.queryUtility(ILogger)
        self.input_file = input_file
        self.output_file = output_file
        self.output_error_file = output_error_file
        self.cfg = get_config()
        mode = self.cfg.SHACL_MODE
        if mode == 'store':
            self.rdf4j = RDF4J(rdf4j_base=self.cfg.RDF4J_BASE)
            self.auth = HTTPBasicAuth(self.cfg.ADMIN_USER, self.cfg.ADMIN_PASS)
        else:
            self.rdf4j = None
            self.auth = None

    def run(self):
        mode = self.cfg.SHACL_MODE

        self.logger.info("Preprocess")
        prep = Preprocess(mode=mode, auth=self.auth, rdf4j=self.rdf4j)
        input_data = prep.load_data(self.input_file)
        error_data = rdflib.graph.Graph()

        self.logger.info("Creating validator")
        validator = Validator(mode, self.auth, self.rdf4j)

        data_conforms = False
        steps = 1

        while not data_conforms:
            self.logger.info(f"Validating Step {steps}")
            self.statistic('Input Data: ', input_data)
            self.logger.info('Call Validation for Input.')

            conforms, report_graph, report_text = validator.validate(input_data)

            self.logger.info('Violations: ' + str(len([i for i in report_graph.triples(
                (None, None, URIRef('http://www.w3.org/ns/shacl#ValidationResult')))])))

            error_data += report_graph

            steps += 1

            shacl_results = report_graph.query(SHACL_RESULTS)

            self.logger.info('Remove invalide nodes.')

            data_conforms = True
            for shacl_result in shacl_results.bindings:
                if 'severity' in shacl_result:
                    sev = shacl_result['severity']
                    if sev == SH.Violation:
                        # something will be removed, check again with the rest
                        data_conforms = False
                        if 'value' in shacl_result:
                            input_data.remove((shacl_result['node'], shacl_result['path'], shacl_result['value']))
                        else:
                            input_data.remove((shacl_result['node'], None, None))
                            input_data.remove((None, shacl_result['node'], None))
                            input_data.remove((None, None, shacl_result['node']))
                    else:
                        self.logger.debug(sev)
                        self.logger.debug('No Violation')
                else:
                    self.logger.debug('No severity')

            input_data.commit()

            self.statistic('Validated Data: ', input_data)

        writer = ResultWriter(mode=mode, auth=self.auth, rdf4j=self.rdf4j)

        writer.write_results(input_data, self.output_file)
        writer.write_results(error_data, self.output_error_file)
        del input_data
        del error_data
        del validator
        del writer

    def statistic(self, stage, graph):
        self.logger.info(stage)
        a = graph.query(NUMBER_OF_QUERY.format('?s a dcat:Dataset'))
        self.logger.info('datasets: ' + a.bindings[0]['count'])
        a = graph.query(NUMBER_OF_QUERY.format('?s a dcat:Distribution'))
        self.logger.info('distributions: ' + a.bindings[0]['count'])
        a = graph.query(NUMBER_OF_QUERY.format('?s ?p ?o'))
        self.logger.info('nodes:' + a.bindings[0]['count'])
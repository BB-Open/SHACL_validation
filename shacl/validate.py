import pyshacl
import rdflib
from rdflib import URIRef
from zope import component

from shacl.constants import BASE_DIR, SHAPE_FILES, NUMBER_OF_DATASETS, SHACL_RESULTS
from shacl.log.log import ILogger
from shacl.namespaces import SH


class Validator:
    """Validator instance"""

    def __init__(self):
        # todo: get shacl as store
        self.first_run = True
        # Import the SHACL rules
        self.validator = pyshacl.rdfutil.load_from_source(str(BASE_DIR / 'shapes' / SHAPE_FILES[0]))

        if len(SHAPE_FILES) > 1:
            for filename in SHAPE_FILES[1:]:
                self.validator = pyshacl.rdfutil.load_from_source(str(BASE_DIR / 'shapes' / filename), g=self.validator)

        self.ont_graph = rdflib.graph.Graph()
        self.ont_graph.parse(str(BASE_DIR / 'shapes' / 'dcat-ap-de-imports.ttl'))

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

    def __init__(self, input, output, output_error, visitor=None):
        # todo: Shacl as store
        self.input = input
        self.output = output
        self.output_error = output_error
        self.logger = component.queryUtility(ILogger)

    def run(self):
        self.logger.info("Creating validator")
        validator = Validator()

        data_conforms = False
        steps = 1

        while not data_conforms:
            self.logger.info("validating")
            conforms, report_graph, report_text = validator.validate(self.input)

            report_graph.serialize(str(self.output_error).format(steps=steps), 'turtle')

            self.logger.info(f'\nstep: {steps}')
            steps += 1

            self.statistic('\nInput Data: ', self.input)

            self.logger.info('\nViolations: ' + str(len([i for i in report_graph.triples(
                (None, None, URIRef('http://www.w3.org/ns/shacl#ValidationResult')))])))

            self.logger.info(report_text)

            shacl_results = report_graph.query(SHACL_RESULTS)

            data_conforms = True
            for shacl_result in shacl_results.bindings:
                if 'severity' in shacl_result:
                    sev = shacl_result['severity']
                    if sev == SH.Violation:
                        # something will be removed, check again with the rest
                        data_conforms = False
                        if 'value' in shacl_result:
                            self.input.remove((shacl_result['node'], shacl_result['path'], shacl_result['value']))
                        else:
                            self.input.remove((shacl_result['node'], None, None))
                            self.input.remove((None, shacl_result['node'], None))
                            self.input.remove((None, None, shacl_result['node']))
                    else:
                        self.logger.info(sev)
                        self.logger.info('No Violation')
                else:
                    self.logger.info('No severity')

            self.input.commit()

            self.statistic('\nValidated Data', self.input)

        self.input.serialize(self.output, 'turtle')

    def statistic(self, stage, graph):
        self.logger.info(stage)
        a = graph.query(NUMBER_OF_DATASETS.format('?s a dcat:Dataset'))
        self.logger.info('datasets: ' + a.bindings[0]['count'])
        a = graph.query(NUMBER_OF_DATASETS.format('?s a dcat:Distribution'))
        self.logger.info('distributions: ' + a.bindings[0]['count'])
        a = graph.query(NUMBER_OF_DATASETS.format('?s ?p ?o'))
        self.logger.info('nodes:' + a.bindings[0]['count'])
import pyshacl
import rdflib
from pkan_config.config import get_config
from rdflib import Namespace

from shacl.constants import BASE_DIR, SHAPE_FILES, QUERY_ALL
from shacl.log.log import get_logger
from pkan_config.namespaces import NAMESPACES
from shacl.ustils.errors import NotAllCasesCovered


def bind_namespaces(graph):
    for namespace_short, namespace in NAMESPACES.items():
        graph.bind(namespace_short, Namespace(namespace))


def load_store_from_rdf4j(database_path, auth, rdf4j):
    graph = rdflib.graph.Graph()
    data = rdf4j.get_triple_data_from_query(database_path,
                                            QUERY_ALL,
                                            auth=auth,
                                            mime_type='application/x-turtle')

    graph_data = graph.parse(data=data, format='turtle')
    bind_namespaces(graph_data)
    return graph_data


def load_store_from_file(file_path):
    graph = rdflib.graph.Graph()
    graph_data = graph.parse(open(file_path, 'rb'))
    bind_namespaces(graph_data)
    return graph_data


def load_shacl_store_from_rdf4j(auth, rdf4j):
    cfg = get_config()
    validator = load_store_from_rdf4j(cfg.SHACL_RULE_DB, auth, rdf4j)
    onto_graph = load_store_from_rdf4j(cfg.SHACL_ONTO_DB, auth, rdf4j)
    bind_namespaces(validator)
    bind_namespaces(onto_graph)
    return validator, onto_graph


def load_shacl_store_from_file():
    validator = pyshacl.rdfutil.load_from_source(str(BASE_DIR / 'shapes' / SHAPE_FILES[0]))

    if len(SHAPE_FILES) > 1:
        for filename in SHAPE_FILES[1:]:
            validator = pyshacl.rdfutil.load_from_source(str(BASE_DIR / 'shapes' / filename), g=validator)

    ont_graph = rdflib.graph.Graph()
    ont_graph.parse(str(BASE_DIR / 'shapes' / 'dcat-ap-de-imports.ttl'), format='turtle')
    bind_namespaces(validator)
    bind_namespaces(ont_graph)
    return validator, ont_graph


class Preprocess:

    def __init__(self, mode='file', auth=None, rdf4j=None):
        """
        mode: file, store
        """
        self.mode = mode
        self.auth = auth
        self.rdf4j = rdf4j
        self.logger = get_logger()

    def load_data(self, input_file):
        self.logger.info(f"Loading {input_file}")
        if self.mode == 'file':
            return load_store_from_file(input_file)
        elif self.mode == 'store':
            return load_store_from_rdf4j(input_file, self.auth, self.rdf4j)
        else:
            NotAllCasesCovered('Unknown Mode')

    # todo: cache this?
    def load_shacl(self):
        if self.mode == 'file':
            return load_shacl_store_from_file()
        elif self.mode == 'store':
            return load_shacl_store_from_rdf4j(self.auth, self.rdf4j)
        else:
            NotAllCasesCovered('Unknown Mode')

from pkan_config.config import get_config
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth

from shacl.log.log import get_logger
from shacl.preprocess import load_shacl_store_from_file
from shacl.results import write_results_to_rdf4j
from shacl.ustils.errors import NotAllCasesCovered


def fill_shacl_db():
    logger = get_logger()
    cfg = get_config()
    mode = cfg.SHACL_MODE
    if mode == 'file':
        pass
    elif mode == 'store':
        logger.info('Filling Shacl Stores started')
        rdf4j = RDF4J(rdf4j_base=cfg.RDF4J_BASE)
        auth = HTTPBasicAuth(cfg.ADMIN_USER, cfg.ADMIN_PASS)
        validator, ont_graph = load_shacl_store_from_file(logger)
        logger.info("Write Onto Graph")
        write_results_to_rdf4j(ont_graph, cfg.SHACL_ONTO_DB, auth, rdf4j)
        logger.info("Write Validator")
        write_results_to_rdf4j(validator, cfg.SHACL_RULE_DB, auth, rdf4j)

        logger.info('Filling Shacl Stores finished')
    else:
        NotAllCasesCovered('Unknown Mode')
from pkan_config.config import get_config
from pyrdf4j.errors import TerminatingError, CannotStartTransaction

from shacl.log.log import get_logger
from shacl.ustils.errors import NotAllCasesCovered


def write_results_to_rdf4j(data, db_name, auth, rdf4j):
    cfg = get_config()
    rdf4j.create_repository(db_name, repo_type=cfg.RDF_REPO_TYPE, overwrite=True, auth=auth)
    data = data.serialize(format='text/turtle')
    if isinstance(data, str):
        data = data.encode('utf-8')

    return rdf4j.add_data_to_repo(
        db_name,
        data,
        'text/turtle',
        auth=auth
    )


def write_results_to_file(data, path):
    data.serialize(path, 'text/turtle')


class ResultWriter:

    def __init__(self, mode='file', auth=None, rdf4j=None):
        """
        mode: file, store
        """
        self.mode = mode
        self.auth = auth
        self.rdf4j = rdf4j
        self.logger = get_logger()

    def write_results(self, data, path,):
        self.logger.info(f"Writing results to {path}")
        if self.mode == 'file':
            write_results_to_file(data, path)
        elif self.mode == 'store':
            try:
                write_results_to_rdf4j(data, path, self.auth, self.rdf4j)
            except TerminatingError as e:
                self.logger.error('Could not write data cause of TerminatingError.')
                self.logger.error(data)
                self.logger.error(e.args)
            except CannotStartTransaction as e:
                self.logger.error('Could not write data cause of CannotStartTransactionError.')
                self.logger.error(data)
                self.logger.error(e.args)
        else:
            NotAllCasesCovered('Unknown Mode')

from shacl.ustils.errors import NotAllCasesCovered


def write_results_to_rdf4j(data, path):
    # todo
    pass


def write_results_to_file(data, path):
    data.serialize(path, 'turtle')


class ResultWriter:

    def __init__(self, mode='file'):
        """
        mode: file, store
        """
        self.mode = mode

    def write_results(self, data, path, replace=True):
        if self.mode == 'file':
            write_results_to_file(data, path)
        elif self.mode == 'store':
            write_results_to_rdf4j(data, path)
        else:
            NotAllCasesCovered('Unknown Mode')

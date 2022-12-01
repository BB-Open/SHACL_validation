import weasyprint
from pkan_config.config import get_config
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth

from shacl.constants import SHACL_RESULTS, TABLE_HEADER, HTML_STYLE, PDF_STYLE
from shacl.log.log import get_logger
from shacl.namespaces import SH
from shacl.preprocess import Preprocess


class HTMLTableReport:

    def __init__(self):
        self.cfg = get_config()
        self.logger = get_logger()
        self.mode = self.cfg.SHACL_MODE
        if self.mode == 'store':
            self.rdf4j = RDF4J(rdf4j_base=self.cfg.RDF4J_BASE)
            self.auth = HTTPBasicAuth(self.cfg.ADMIN_USER, self.cfg.ADMIN_PASS)
        else:
            self.rdf4j = None
            self.auth = None

    def get_row(self, data):
        return """<tr style="background-color: {color}">
    <td>{severity}</td>
    <td>{amount}</td>
    <td>{msg}</td>
    <td>{sourceConstraintComponent}</td>
    <td>{sourceShape}</td>
    <td>{node}</td>
    <td>{path}</td>
    <td>{value}</td></tr>
        
        """.format(**data)

    def collect_data(self, error_path):
        # reports will be generated on demand, so stores are reloaded
        prep = Preprocess(mode=self.mode, auth=self.auth, rdf4j=self.rdf4j)
        report_graph = prep.load_data(error_path)
        shacl_results = report_graph.query(SHACL_RESULTS)

        report_data = {}

        # collecting data
        for shacl_result in shacl_results.bindings:

            sev = shacl_result['severity']
            if not sev in report_data:
                report_data[sev] = {}
            sConstraintComponent = shacl_result['sourceConstraintComponent']
            if not sConstraintComponent in report_data[sev]:
                report_data[sev][sConstraintComponent] = {}
            sShape = shacl_result['sourceShape']
            if not sShape in report_data[sev][sConstraintComponent]:
                report_data[sev][sConstraintComponent][sShape] = {}
            if 'msg' in shacl_result:
                msg = shacl_result['msg']
            else:
                msg = ''
            if not msg in report_data[sev][sConstraintComponent][sShape]:
                report_data[sev][sConstraintComponent][sShape][msg] = []

            node = shacl_result['node']
            path = shacl_result['path']
            if 'value' in shacl_result:
                value = shacl_result['value']
            else:
                value = ''
            report_data[sev][sConstraintComponent][sShape][msg].append({
                'node': node,
                'path': path,
                'value': value
            })
        return report_data

    def render_rows(self, report_data, display_details):

        statistics_rows = ''
        detail_rows = ''

        for sev, sConstraintComponents in report_data.items():
            color = 'white'
            sev_name = sev
            if sev == SH.Violation:
                sev_name = 'Violation'
                color = '#ffe6e6'
            elif sev == SH.Warning:
                sev_name = 'Warning'
                color = '#ffeecc'
            elif sev == SH.Info:
                sev_name = 'Info'
                color = '#f2ffcc'
            for sConstraintComponent, sShapes in sConstraintComponents.items():
                for sShape, messages in sShapes.items():
                    for message, data in messages.items():
                        unpacked_data = {'severity': sev_name,
                                         'color': color,
                                         'msg': message,
                                         'sourceConstraintComponent': sConstraintComponent,
                                         'amount': len(data),
                                         'sourceShape': sShape,
                                         }
                        unpacked_data.update(data[0])
                        statistics_rows += self.get_row(
                            unpacked_data
                        )
                        if display_details:
                            unpacked_data['amount'] = 1
                            for detail in data:
                                unpacked_data.update(detail)
                                detail_rows += self.get_row(
                                    unpacked_data
                                )

        return detail_rows, statistics_rows

    def render_report_data(self, report_data, display_details):
        statistic_rows, detail_rows = self.render_rows(report_data, display_details)
        statistics = TABLE_HEADER + statistic_rows + '</table>'
        details = TABLE_HEADER + detail_rows + '</table>'
        return details, statistics

    def generate(self, error_path, target_path=None, display_details=False, raw=True):
        self.logger.info('Generate HTML')
        report_data = self.collect_data(error_path)

        # render data
        details, statistics = self.render_report_data(report_data, display_details)

        if not display_details:
            details = '<p>Details deactivated</p>'

        html = f"""
            <html>
            <head>
                {HTML_STYLE}
            </head>
            <body>
            <h1>Report for {error_path}</h1>
            <h2>Statistics</h2>
            {statistics}
            <h2>Detailed Report</h2>
            {details}
            </body>
            </html>
"""

        if target_path:
            self.logger.info(f'Write Results to Path {target_path}')
            f = open(target_path, 'w')

            f.write(html)
            f.close()

        if raw:
            return details
        else:
            return html


class HTMLBlockReport(HTMLTableReport):

    def get_row(self, data):
        return """<div style="background-color: {color}">
        <h3>{severity}: {msg} [{amount} occurrences]</h3>
        <p>Details</p>
        <ul>
            <li>sourceConstraintComponent: {sourceConstraintComponent}</li>
            <li>sourceShape: {sourceShape}</li>
            <li>node: {node}</li>
            <li>path: {path}</li>
            <li>value: {value}</li>
        </ul>
        </div>
        """.format(**data)

    def render_report_data(self, report_data, display_details):
        return self.render_rows(report_data, display_details)


class PDFTableReport:

    def __init__(self):
        self.cfg = get_config()
        self.logger = get_logger()
        self.html_report = HTMLTableReport()

    def generate(self, error_path, target_path=None, display_details=False):
        # use html and convert it
        html = self.html_report.generate(error_path, display_details=display_details, raw=False)
        self.logger.info('Convert HTML to PDF')
        style = weasyprint.CSS(string=PDF_STYLE)
        pdf = weasyprint.HTML(string=html).write_pdf(stylesheets=[style])

        self.logger.info(f'Write Results to Path {target_path}')
        f = open(target_path, 'wb')

        f.write(pdf)
        f.close()


class PDFBlockReport(PDFTableReport):

    def __init__(self):
        super().__init__()
        self.html_report = HTMLBlockReport()

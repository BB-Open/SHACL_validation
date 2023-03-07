import tempfile

import weasyprint
from pkan_config.config import get_config
from pyrdf4j.rdf4j import RDF4J
from requests.auth import HTTPBasicAuth

from shacl.constants import SHACL_RESULTS, TABLE_HEADER, HTML_STYLE, PDF_STYLE, TABLE_PDF_STYLE, BLOCKS_PDF_STYLE, \
    COLORS, SEVS, COMPARISON_TABLE_HEADER, SHACL_FILES_TABLE_HEADER, SHAPE_FILES, SHAPE_FILES_META
from shacl.log.log import get_logger
from pkan_config.namespaces import SH
from shacl.preprocess import Preprocess


def clear_entry(entry, ns_manager):
    if entry == SH.Violation:
        return 'Fehler'
    elif entry == SH.Warning:
        return 'Warnung'
    elif entry == SH.Info:
        return 'Info'
    else:
        res = entry.n3(ns_manager)
        res = res.replace('<', '&#60;')
        res = res.replace('>', '&#62;')
        return res


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

    def get_overview(self, overview_data, provider, date, comparison_fields):
        overview_html = ''
        if provider or date:
            overview_html += '<h3>Details der Erzeugung</h3><div>'
            if provider:
                overview_html += f"<p><i>Datenbereitsteller:</i> {provider}</p>"
            if date:
                overview_html += f"<p><i>Zeitpunkt der Erfassung:</i> {date}</p>"
            overview_html += '</div>'
        overview_html += '<h3>Meldungen</h3><div>'
        for sev in SEVS:
            if sev in overview_data:
                overview_html += f"<p><i>{sev}:</i> {overview_data[sev]}</p>"
            else:
                overview_html += f"<p><i>{sev}:</i> 0</p>"
        overview_html += '</div>'
        if comparison_fields:
            overview_html += '<h3>Datenvergleich</h3>'
            overview_html += COMPARISON_TABLE_HEADER
            for field in comparison_fields:
                overview_html += "<tr><td>{field}</td><td>{old}</td><td>{new}</td></tr>".format(**field)
            overview_html += '</table>'
        overview_html += '<h3>Shacl Dateien</h3>'
        overview_html += SHACL_FILES_TABLE_HEADER
        for filename in SHAPE_FILES:
            meta = SHAPE_FILES_META[filename]
            overview_html += f"<tr><td>{filename}</td><td>{meta['version']}</td><td>{meta['last_change']}</td><td>{meta['last_download']}</td></tr>"
        overview_html += '</table>'
        return overview_html

    def get_row(self, data):
        return """<tr style="background-color: {color}">
    <td>{severity}</td>
    <td>{occurrence}</td>
    <td>{msg}</td>
    <td>{sourceShape}</td>
    <td>{sourceConstraintComponent}</td>
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
        overview_data = {}

        # collecting data
        for shacl_result in shacl_results.bindings:

            sev = clear_entry(shacl_result['severity'], report_graph.namespace_manager)
            if sev in overview_data:
                overview_data[sev] += 1
            else:
                overview_data[sev] = 1
            if not sev in report_data:
                report_data[sev] = {}
            sConstraintComponent = clear_entry(shacl_result['sourceConstraintComponent'],
                                               report_graph.namespace_manager)
            if not sConstraintComponent in report_data[sev]:
                report_data[sev][sConstraintComponent] = {}
            sShape = clear_entry(shacl_result['sourceShape'], report_graph.namespace_manager)
            if not sShape in report_data[sev][sConstraintComponent]:
                report_data[sev][sConstraintComponent][sShape] = []

            if 'msg' in shacl_result:
                msg = clear_entry(shacl_result['msg'], report_graph.namespace_manager)
            else:
                msg = ''

            node = clear_entry(shacl_result['node'], report_graph.namespace_manager)
            path = clear_entry(shacl_result['path'], report_graph.namespace_manager)
            if 'value' in shacl_result:
                value = clear_entry(shacl_result['value'], report_graph.namespace_manager)
            else:
                value = ''
            report_data[sev][sConstraintComponent][sShape].append({
                'node': node,
                'path': path,
                'value': value,
                'msg': msg
            })
        del report_graph
        del shacl_result
        return report_data, overview_data

    def render_rows(self, report_data, display_details):

        statistics_rows = {}
        detail_rows = ''
        counter = 0

        for sev, sConstraintComponents in report_data.items():
            color = 'white'
            if sev in COLORS:
                color = COLORS[sev]
            for sConstraintComponent, sShapes in sConstraintComponents.items():
                for sShape, data in sShapes.items():
                    occurrence = len(data)
                    unpacked_data = {'severity': sev,
                                     'color': color,
                                     'sourceConstraintComponent': sConstraintComponent,
                                     'occurrence': len(data),
                                     'sourceShape': sShape,
                                     }
                    unpacked_data.update(data[0])
                    unpacked_data['occurrence_formatted'] = f'[{unpacked_data["occurrence"]} Fälle] '
                    if occurrence in statistics_rows:
                        statistics_rows[occurrence] += self.get_row(
                            unpacked_data
                        )
                    else:
                        statistics_rows[occurrence] = self.get_row(unpacked_data)
                    if display_details:
                        unpacked_data['occurrence_formatted'] = ''
                        unpacked_data['occurrence'] = 1
                        for detail in data:
                            if counter < self.cfg.MAXIMUM_DETAIL_ERROR:
                                unpacked_data.update(detail)
                                detail_rows += self.get_row(
                                    unpacked_data
                                )
                                counter += 1
                            else:
                                break
        # sort statistics_rows by occurences
        occurrences = list(statistics_rows.keys())
        occurrences_sorted = sorted(occurrences, reverse=True)

        statistics_rows_sorted = ''
        for occ in occurrences_sorted:
            statistics_rows_sorted += statistics_rows[occ]

        return detail_rows, statistics_rows_sorted

    def render_report_data(self, report_data, display_details):
        statistic_rows, detail_rows = self.render_rows(report_data, display_details)
        statistics = TABLE_HEADER + statistic_rows + '</table>'
        details = TABLE_HEADER + detail_rows + '</table>'
        return details, statistics

    def generate(self, error_path, target_path=None, display_details=False, raw=True, comparison_fields=None,
                 provider='', date='', title=''):
        self.logger.info('Generate HTML')
        report_data, overview_data = self.collect_data(error_path)

        # overview
        overview = self.get_overview(overview_data, provider, date, comparison_fields)
        # render data
        details, statistics = self.render_report_data(report_data, display_details)

        del report_data
        del overview_data

        if not display_details:
            details = '<p>Details wurden deaktiviert</p>'

        if not title:
            title = error_path

        html = f"""
            <html>
            <head>
                <style>
                {HTML_STYLE}
                </style>
            </head>
            <body>
            <h1>Report für {title}</h1>
            <h2>Übersicht</h2>
            {overview}
            <h2>Aggregierter Report</h2>
            {statistics}
            <h2>Detaillierter Report [Maximal {self.cfg.MAXIMUM_DETAIL_ERROR} Fehler]</h2>
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
        <h3>{occurrence_formatted}{severity}: {msg}</h3>
        <p style="font-weight: bold;">Test</p>
        <p><i>Regel:</i> {sourceShape}</p>
        <p><i>Bedingung:</i> {sourceConstraintComponent}</p>
        <p style="font-weight: bold;">Ort</p>
        <p><i>Knoten:</i> {node}</p>
        <p><i>Pfad:</i> {path}</p>
        <p><i>Wert:</i> {value}</p>
        </div>
        """.format(**data)

    def render_report_data(self, report_data, display_details):
        return self.render_rows(report_data, display_details)


class PDFTableReport:

    def __init__(self):
        self.cfg = get_config()
        self.logger = get_logger()
        self.html_report = HTMLTableReport()
        self.special_style = TABLE_PDF_STYLE

    def generate(self, error_path, target_path=None, display_details=False, comparison_fields=None, provider='',
                 date='', title=''):
        # use html and convert it
        html = self.html_report.generate(error_path, display_details=display_details, raw=False,
                                         comparison_fields=comparison_fields, provider=provider, date=date, title=title)
        self.logger.info('Convert HTML to PDF')
        common_style = weasyprint.CSS(string=PDF_STYLE)
        special_style = weasyprint.CSS(string=self.special_style)
        pdf = weasyprint.HTML(string=html).write_pdf(stylesheets=[common_style, special_style])

        self.logger.info(f'Write Results to Path {target_path}')
        f = open(target_path, 'wb')

        f.write(pdf)
        f.close()


class PDFBlockReport(PDFTableReport):

    def __init__(self):
        super().__init__()
        self.html_report = HTMLBlockReport()
        self.special_style = BLOCKS_PDF_STYLE

import click
import datetime
import json
import requests
import uuid
from ga4gh.htsget.compliance.config.tests import TEST_GROUPS
from ga4gh.htsget.compliance.config import constants as c
from ga4gh.htsget.compliance.methods.test_api_response import test_api_response
from ga4gh.testbed.models.report import Report
from ga4gh.testbed.models.report_group import ReportGroup

@click.command()
@click.argument("htsget_url")
@click.option('-f', '--file', help="report written to output file")
@click.option('-t', '--testbed-url', 
    help="report submitted as POST request body to GA4GH testbed service")
def main(**kwargs):

    uniqid = str(uuid.uuid1())
    configuration_id = "5e27341e58496513e01c6510"
    report = Report()
    report.set_id(uniqid)
    report.set_configuration_id(configuration_id)
    report.set_parameters(kwargs)

    for endpoint in c.ENDPOINTS:
        group = ReportGroup()
        group.set_name(endpoint)
        cases = TEST_GROUPS[endpoint]["cases"]
        for case in cases:
            case = test_api_response(case, kwargs)
            group.add_case(case)
        group.summarize()
        report.add_group(group)
    
    report.finalize()
    if kwargs["file"] or kwargs["testbed_url"]:
        if kwargs["file"]:
            open(kwargs["file"], 'w').write(str(report))
        elif kwargs["testbed_url"]:
            requests.post(kwargs["testbed_url"], json=report.as_json())
    else:
        print(str(report))

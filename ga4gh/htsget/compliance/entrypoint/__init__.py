# -*- coding: utf-8 -*-
"""htsget compliance program entrypoint

Example:
    Once installed, program can be executed from command line via::

        $ htsget-compliance ${HTSGET_BASE_URL}

Todo:
    * better handling of uniqid for report
    * remove hardcoded configuration id, get configuration id from testbed
"""

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
    """program entrypoint method, runs compliance tests against htsget service

    Args:
        kwargs (dict): input arguments/options parsed from command line
    """

    # create the Report object, initialize with unique report id, and 
    # hardcoded configuration id
    uniqid = str(uuid.uuid1())
    configuration_id = "5e27341e58496513e01c6510"
    report = Report()
    report.set_id(uniqid)
    report.set_configuration_id(configuration_id)
    report.set_parameters(kwargs)

    # for each endpoint (reads, variants), create an empty ReportGroup. Run all
    # test cases in the associated test group, and add each ReportCase to the 
    # ReportGroup. Finally, summarize ReportGroup and add it to the Report
    for endpoint in c.ENDPOINTS:
        group = ReportGroup()
        group.set_name(endpoint)
        cases = TEST_GROUPS[endpoint]["cases"]
        for case in cases:
            case = test_api_response(case, kwargs)
            group.add_case(case)
        group.summarize()
        report.add_group(group)
    
    # summarize the Report
    report.finalize()
    
    # write report to file and/or submit report as POST request to testbed
    if kwargs["file"] or kwargs["testbed_url"]:
        if kwargs["file"]:
            open(kwargs["file"], 'w').write(str(report))
        elif kwargs["testbed_url"]:
            requests.post(kwargs["testbed_url"], json=report.as_json())
    # print report if it's neither written to file or sent to testbed
    else:
        print(str(report))

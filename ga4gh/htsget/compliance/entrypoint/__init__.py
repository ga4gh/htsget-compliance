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
from ga4gh.htsget.compliance.config.test_case_property_matrix \
    import construct_reads_test_cases_matrix
from ga4gh.htsget.compliance.methods.test_api_response import test_api_response
from ga4gh.htsget.compliance.test_case import TestCase
from ga4gh.testbed.models.report import Report
from ga4gh.testbed.models.report_group import ReportGroup

@click.command()
@click.argument("htsget-url")
@click.option('-r', '--reads-base-path',
              help="base url path to 'reads' requests",
              default=c.DEFAULT_READS_URLPATH)
@click.option('-v', '--variants-base-path',
              help="base url path to 'variants' requests",
              default=c.DEFAULT_VARIANTS_URLPATH)
@click.option('-f', '--file', help="report written to output file")
@click.option('-s', '--submit', is_flag = True, help='Submit JSON report to testbedAPI')
@click.option(
    '--submit-id', help='report series ID required by GA4GH testbed')  
@click.option(
    '--submit-token', help='report series token required by GA4GH testbed') 
@click.option(
    '-t', '--testbed-url', default="http://localhost:4500/reports", help='submit report to GA4GH testbed service')
def main(**kwargs):
    """run compliance tests against htsget service"""

    # create the Report object, initialize with unique report id, and 
    # hardcoded configuration id
    uniqid = str(uuid.uuid1())
    configuration_id = "5e27341e58496513e01c6510"
    report = Report()
    report.set_id(uniqid)
    report.set_configuration_id(configuration_id)
    params = {'server': kwargs["htsget_url"]}
    report.set_parameters(params)

    # for each endpoint (reads, variants), create an empty ReportGroup. Run all
    # test cases in the associated test group, and add each ReportCase to the 
    # ReportGroup. Finally, summarize ReportGroup and add it to the Report

    reads_test_cases = construct_reads_test_cases_matrix()

    for endpoint in c.ENDPOINTS:
        group = ReportGroup()
        group.set_name(endpoint)
        group.set_start_time(str(datetime.datetime.utcnow().strftime(c.TIMESTAMP_FORMAT)))
        cases = TEST_GROUPS[endpoint]["cases"]
        for case_props in cases:
            test_case_obj = TestCase(case_props, kwargs)
            report_case = test_case_obj.execute_test()
            group.add_case(report_case)

        group.set_end_time(str(datetime.datetime.utcnow().strftime(c.TIMESTAMP_FORMAT)))
        group.summarize()
        report.add_group(group)
    
    # summarize the Report
    report.finalize()
    
    # write report to file
    if kwargs["file"]:
        if kwargs["file"]:
            open(kwargs["file"], 'w').write(str(report.as_json()))

    # submit report to testbed
    if kwargs["testbed_url"] and kwargs["submit"] and kwargs["submit_id"] and kwargs["submit_token"]:
        print("Attempting to submit to testbed API...")
        header = {"GA4GH-TestbedReportSeriesId": kwargs["submit_id"], "GA4GH-TestbedReportSeriesToken": kwargs["submit_token"]}
        response = requests.post(kwargs["testbed_url"], headers=header, json=json.loads(str(report)))
        if response.status_code == 200:
            # prints the submit ID for the report from the testbed service
            print("The submission was successful, the report ID is " + response.json()["id"])
        else:
            print("The submission failed with a status code of " + str(response.status_code))
            print("Error Message: " + str(response.content))
    
    # print report if it's neither written to file or sent to testbed
    if not kwargs["submit"] or not kwargs["file"]:
        print(str(report))

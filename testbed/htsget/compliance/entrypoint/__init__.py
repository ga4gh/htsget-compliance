# -*- coding: utf-8 -*-
"""htsget compliance program entrypoint

Example:
    Once installed, program can be executed from command line via::

        $ htsget-compliance ${HTSGET_BASE_URL}

Todo:
    * better handling of uniqid for report
    * remove hardcoded configuration id, get configuration id from testbed
"""

from typing import final
import click
import datetime
import json
import requests
import uuid
from testbed.htsget.compliance.config.tests import TEST_GROUPS
from testbed.htsget.compliance.config import constants as c
from testbed.htsget.compliance.config.test_case_property_matrix \
    import construct_reads_test_cases_matrix
from testbed.htsget.compliance.methods.test_api_response import test_api_response
from testbed.htsget.compliance.test_case import TestCase
from ga4gh.testbed.report.report import Report
from ga4gh.testbed.submit.report_submitter import ReportSubmitter

from testbed.htsget.compliance.test_runner import TestRunner

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
    '--submit-id', help='report series ID')  
@click.option(
    '--submit-token', help='report series token') 
@click.option(
    '-t', '--testbed-url', default="http://localhost:4500/reports", help='submit report to GA4GH testbed service')
def main(**kwargs):
    """run compliance tests against htsget service"""

    # create the Report object, initialize with unique report id, and 
    # hardcoded configuration id
    # uniqid = str(uuid.uuid1())
    # configuration_id = "5e27341e58496513e01c6510"
    # report = Report()
    # report.set_id(uniqid)
    # report.set_configuration_id(configuration_id)
    # report.set_parameters(kwargs)

    # for each endpoint (reads, variants), create an empty ReportGroup. Run all
    # test cases in the associated test group, and add each ReportCase to the 
    # ReportGroup. Finally, summarize ReportGroup and add it to the Report

    # reads_test_cases = construct_reads_test_cases_matrix()

    # for endpoint in c.ENDPOINTS:
    #     group = ReportGroup()
    #     group.set_name(endpoint)
    #     cases = TEST_GROUPS[endpoint]["cases"]
    #     for case_props in cases:
    #         test_case_obj = TestCase(case_props, kwargs)
    #         report_case = test_case_obj.execute_test()
    #         group.add_case(report_case)
    #     group.summarize()
    #     report.add_group(group)
    
    # # summarize the Report
    # report.finalize()

    tr = TestRunner(kwargs["htsget_url"])
    tr.run_tests()

    ga4gh_report = tr.generate_report()
    final_json = ga4gh_report.to_json(pretty=True)
    final_json = json.loads(final_json)
    footer = {"testbed": {
        "id": "htsget-compliance",
        "testbed_name": "Htsget Compliance Suite",
        "testbed_description": "Test compliance of htsget services to specification",
        "repo_url": "https://github.com/ga4gh/htsget-compliance-suite",
        "dockerhub_url": "",
        "dockstore_url": ""
            }
        }

    final_json.update(footer)
    final_json = json.dumps(final_json)   
    
    # write report to file
    if kwargs["file"]:
        if kwargs["file"]:
            open(kwargs["file"], 'w').write(str(final_json))

    # submit report to testbed
    if kwargs["testbed_url"] and kwargs["submit"] and kwargs["submit_id"] and kwargs["submit_token"]:
        print("Attempting to submit to testbed API...")
        response = ReportSubmitter.submit_report(kwargs["submit_id"], kwargs["submit_token"], final_json, url=kwargs["testbed_url"])
        if response["status_code"] == 200:
            print("The submission was successful, the report ID is " + response["report_id"])
        else:
            print("The submission failed with a status code of " + str(response["status_code"]))
            print("Error Message: " + str(response["error_message"]))
    
    # print report if it's neither written to file or sent to testbed
    if not kwargs["submit"] or not kwargs["file"]:
        print(str(final_json))

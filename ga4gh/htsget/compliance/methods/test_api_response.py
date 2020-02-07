# -*- coding: utf-8 -*-
"""generalized method for testing api compliance

The method(s) contained herein are run for each test case. Broadly, they make
an API request based on test case parameters and test: that response code 
matches expected, that JSON response matches the htsgetResponse JSON schema.
"""

import json
import requests
from ga4gh.htsget.compliance.config import constants as c
from ga4gh.htsget.compliance.schema_validator import SchemaValidator
from ga4gh.testbed.models.report_case import ReportCase

def test_api_response(test_case, kwargs):
    """Makes api request and tests response for compliance

    Args:
        test_case (dict): outlines test case name, target url, and expected
            results. expected results include response code.
        kwargs (dict): web-service specific information, provided on commandline

    Returns:
        ReportCase: reports on whether test case was successful or not, and why
    """

    # instantiate ReportCase
    report_case = ReportCase()
    report_case.set_name(test_case["name"])
    
    try:
        # setup target url from template
        url = test_case["urlfunc"](test_case, kwargs)
        
        response = requests.get(url)
        # validate the response status code matches expected according to
        # test case
        if test_case["resp_status"] != response.status_code:
            raise Exception("incorrect status code")

        # parse returned JSON from response, and validate it against the
        # schema
        response_json = response.json()
        sv = SchemaValidator()
        validation_result = sv.validate_instance(response_json)
        if validation_result["status"] == SchemaValidator.FAILURE:
            raise Exception(validation_result["message"])

        report_case.set_status_success()
        
    except Exception as e:
        # any raised exceptions will set the ReportCase status to failure
        report_case.set_status_failure()
        report_case.set_error(str(e))
    
    return report_case

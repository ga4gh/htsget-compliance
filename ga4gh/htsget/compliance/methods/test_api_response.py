import json
import requests
from ga4gh.htsget.compliance.config import constants as c
from ga4gh.htsget.compliance.schema_validator import SchemaValidator
from ga4gh.testbed.models.report_case import ReportCase

def test_api_response(test_case, config):

    report_case = ReportCase()
    report_case.set_name(test_case["name"])
    
    try:
        url_template = test_case['url']
        url_dict = {
            "base_url": config["htsget_url"],
            "obj_id": test_case["obj_id"]
        }
        url = url_template.format(**url_dict)
        
        response = requests.get(url)
        if test_case["resp_status"] != response.status_code:
            raise Exception("incorrect status code")

        response_json = response.json()
        sv = SchemaValidator()
        validation_result = sv.validate_instance(response_json)
        if validation_result["status"] == SchemaValidator.FAILURE:
            raise Exception(validation_result["message"])
        
    except Exception as e:
        report_case.set_status_failure()
        report_case.set_error(str(e))
    
    return report_case

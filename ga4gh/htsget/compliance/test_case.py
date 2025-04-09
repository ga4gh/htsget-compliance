# -*- coding: utf-8 -*-
"""A single test run against an htsget server"""

import datetime
from ga4gh.htsget.compliance.config import constants as c
from ga4gh.htsget.compliance.config import methods
from ga4gh.htsget.compliance.schema_validator import SchemaValidator
from ga4gh.htsget.compliance.file_validator import FileValidator
from ga4gh.htsget.compliance.filepart_aggregator import FilepartAggregator
from ga4gh.testbed.models.report_case import ReportCase

class TestCase(object):

    def __init__(self, props, kwargs):
        """Instantiates a TestCase object"""
        
        self.set_name(props["name"])
        self.set_url_function(props["url_function"])
        self.set_url_params(props["url_params"])
        self.set_obj_id(props["obj_id"])
        self.set_expected_response_status(props["expected_response_status"])
        self.set_expected_contents(props["expected_contents"])
        self.expected_key = props["expected_key"]
        self.set_kwargs(kwargs)

    def validate_response_code(self, responses: list):
        for response in responses:
            if not (200 <= response.status_code <= 308):
                if self.get_expected_response_status() != response.status_code:
                    raise Exception("incorrect status code meow")
    
    def validate_response_schema(self, response):
        response_json = response.json()
        sv = SchemaValidator()
        validation_result = sv.validate_instance(response_json)
        if validation_result["status"] == SchemaValidator.FAILURE:
            raise Exception(validation_result["message"])
    
    def validate_file_contents(self, response, payload, params=None):
        aggregator = FilepartAggregator(response)
        aggregator.aggregate(params)
        returned_filepath = aggregator.get_output_filepath()
        expected_filepath = self.get_expected_contents()
        file_validator = FileValidator(returned_filepath, expected_filepath, self.expected_key)
        validation_result = file_validator.validate()
        if validation_result == FileValidator.FAILURE:
            raise Exception("returned file does not match expected")
    
    def execute_test(self):
        
        report_case = ReportCase()
        report_case.set_name(self.get_name())
        report_case.set_start_time(str(datetime.datetime.utcnow().strftime(c.TIMESTAMP_FORMAT)))
        try:
            url = self.get_formatted_url()
            params = self.get_url_params()
            report_case.add_debug_msg("URL: " + url)
            report_case.add_debug_msg("PARAMS: " + str(params))
            # Handle multiple urls and "data:" url types, iterates through all urls returned by htsget
            payload, responses = methods.fetch_url(url, params)
            # First request to the "top-level" htsget endpoint, not the individual urls in the response
            htsget_response = responses[0]
            # Check whether there's an error code in any of the responses for each url queried above
            self.validate_response_code(responses)
            # Validate the htsget response schema, not the payload of the individual URLs
            self.validate_response_schema(htsget_response)
            # Check against samtools (and crypt4gh) with local files fetched on the filesystem
            self.validate_file_contents(htsget_response, payload, params=params)
            report_case.set_status_success()

        except Exception as e:
            # any raised exceptions will set the ReportCase status to failure
            report_case.set_status_failure()
            report_case.set_error(str(e))
        report_case.add_case(report_case)
        report_case.summarize()
        report_case.set_end_time(str(datetime.datetime.utcnow().strftime(c.TIMESTAMP_FORMAT)))

        return report_case
    
    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def set_url_function(self, url_function):
        self.url_function = url_function
    
    def get_url_function(self):
        return self.url_function

    def set_url_params(self, url_params):
        self.url_params = url_params
    
    def get_url_params(self):
        return self.url_params
    
    def get_formatted_url(self):
        func = self.get_url_function()
        return func(self.get_props_dict(), self.get_kwargs())
    
    def set_obj_id(self, obj_id):
        self.obj_id = obj_id
    
    def get_obj_id(self):
        return self.obj_id
    
    def set_expected_response_status(self, expected_response_status):
        self.expected_response_status = expected_response_status
    
    def get_expected_response_status(self):
        return self.expected_response_status

    def set_expected_contents(self, expected_contents):
        self.expected_contents = expected_contents

    def get_expected_contents(self):
        return self.expected_contents
    
    def get_props_dict(self):
        return {
            "name": self.get_name(),
            "url_function": self.get_url_function(),
            "obj_id": self.get_obj_id(),
            "expected_response_status": self.get_expected_response_status()
        }
    
    def set_kwargs(self, kwargs):
        self.kwargs = kwargs
    
    def get_kwargs(self):
        return self.kwargs

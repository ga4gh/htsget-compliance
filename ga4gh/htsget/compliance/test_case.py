# -*- coding: utf-8 -*-
"""A single test run against an htsget server"""

import json
import requests
from ga4gh.htsget.compliance.config import constants as c
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
        self.set_kwargs(kwargs)
    
    def validate_response_code(self, response):
        if self.get_expected_response_status() != response.status_code:
            raise Exception("incorrect status code")
    
    def validate_response_schema(self, response):
        response_json = response.json()
        sv = SchemaValidator()
        validation_result = sv.validate_instance(response_json)
        if validation_result["status"] == SchemaValidator.FAILURE:
            raise Exception(validation_result["message"])
    
    def validate_file_contents(self, response):
        aggregator = FilepartAggregator(response)
        aggregator.aggregate()
        returned_filepath = aggregator.get_output_filepath()
        expected_filepath = self.get_expected_contents()
        file_validator = FileValidator(returned_filepath, expected_filepath)
        validation_result = file_validator.validate()
        if validation_result == FileValidator.FAILURE:
            raise Exception("returned file does not match expected")
    
    def execute_test(self):
        
        report_case = ReportCase()
        report_case.set_name(self.get_name())

        try:
            url = self.get_formatted_url()
            params = self.get_url_params()
            report_case.add_debug_msg("URL: " + url)
            report_case.add_debug_msg("PARAMS: " + str(params))
            response = requests.get(url, params=params)
            self.validate_response_code(response)
            self.validate_response_schema(response)
            self.validate_file_contents(response)
            report_case.set_status_success()

        except Exception as e:
            # any raised exceptions will set the ReportCase status to failure
            report_case.set_status_failure()
            report_case.set_error(str(e))
        
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

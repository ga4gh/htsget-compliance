# -*- coding: utf-8 -*-
"""Testbed Report, high level Report containing multiple groups and cases"""

import datetime
import json
from ga4gh.testbed.models.report_summary import ReportSummary

class Report(object):
    """High level report containing multiple groups and cases

    Attributes:
        id (str): unique report identifier
        configuration_id (str): Testbed configuration id this report is based on
        parameters (dict): input parameter values for this report run
        generated_at (str): ISO 8601 timestamp
        summary (ReportSummary): summary of all cases from all groups
        groups (list): list of ReportGroup objects associated with report
    """
    
    def __init__(self):
        self.id = None
        self.configuration_id = None
        self.parameters = {}
        self.generated_at = None
        self.summary = None
        self.groups = []

    def set_id(self, uniqid):
        """set id

        Args:
            uniqid (str): unique id for report
        """

        self.id = uniqid
    
    def get_id(self):
        """get id

        Returns:
            str: report id
        """

        return self.id
    
    def set_configuration_id(self, configuration_id):
        """set configuration id

        Args:
            configuration_id (str): configuration id
        """

        self.configuration_id = configuration_id
    
    def get_configuration_id(self):
        """get configuration id

        Returns:
            str: configuration id
        """

        return self.configuration_id
    
    def set_parameters(self, parameters):
        """set report parameters

        Args:
            parameters (dict): report input parameters for this run
        """

        self.parameters = parameters
    
    def get_parameters(self):
        """get report parameters

        Returns:
            dict: input parameters for this run
        """

        return self.parameters

    def summarize(self):
        """Summarize completed test report cases for all groups

        Aggregates ReportSummary objects for each group in the Report's "groups"
        list into a single ReportSummary. Sets this to the Report object's
        "summary" attribute
        """

        summary = ReportSummary()
        [summary.add_from_summary(group.summary) for group in self.groups]
        self.summary = summary

    def add_group(self, group_obj):
        """Add a group object to the "groups" list

        Args:
            group_obj (ReportGroup): ReportGroup object to add
        """

        self.groups.append(group_obj)
    
    def finalize(self):
        """Finalizes the Report object before outputting

        This method should be run to finalize the report before outputting.
        Finalize sets the timestamp to the current time, as well as generates
        the final summary of all ReportGroups.
        """

        self.generated_at = str(datetime.datetime.now().isoformat())
        self.summarize()

    def as_json(self):
        """Dump Report object as simple python dictionary

        Returns:
            dict: Report object as python dictionary
        """

        return {
            "id": self.get_id(),
            "configurationId": self.get_configuration_id(),
            "parameters": self.get_parameters(),
            "generatedAt": self.generated_at,
            "summary": self.summary.as_json(),
            "groups": [group.as_json() for group in self.groups]
        }
    
    def __str__(self):
        """Represent Report as a string

        Overrides default __str__ method, exports the Report as a JSON string,
        to be written to a file and/or sent as POST request to a testbed
        service.

        Returns:
            str: Report object as JSON string
        """

        return json.dumps(self.as_json())

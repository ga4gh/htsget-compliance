# -*- coding: utf-8 -*-
"""Testbed ReportGroup, reports on a semantically-grouped set of test cases"""

import json
from ga4gh.testbed import constants as c
from ga4gh.testbed.models.report_summary import ReportSummary

class ReportGroup(object):
    """Reports on a semantically-grouped set of test cases

    Attributes:
        name (str): group name
        summary (ReportSummary): summary of all test cases within group
        cases (list): list of ReportCases associated with this group
    """
    
    def __init__(self):
        """Instantiates a ReportGroup object"""

        self.name = None
        self.summary = None
        self.cases = []
        self.start_time = None
        self.end_time = None
        self.status = None

    def add_case(self, case_obj):
        """add a ReportCase to the group

        Args:
            case_obj (ReportCase): object to add to group
        """

        self.cases.append(case_obj)
    
    def set_name(self, name):
        """set group name

        Args:
            name (str): group name
        """

        self.name = name

    def get_name(self):
        """get group name

        Returns:
            str: group name
        """

        return self.name

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_end_time(self, end_time):    
        self.end_time = end_time
    
    def summarize(self):
        """Summarize completed test report cases for the entire group

        Once all ReportCase objects in the group's "cases" list are completed
        (ie. validation methods have been run and case object properties
        finalized), this method will summarize/aggregate the pass,failure,
        warning, skipped counts into a single ReportSummary object, which is
        then set to the 'summary' property.
        """

        def increment_summary(summary_obj, case_obj):
            """increment ReportSummary count was ReportCase status

            Whatever the status of the case object, the corresponding property
            will be incremented by 1 in the summary object

            Args:
                summary_obj (ReportSummary): summary object to increment
                case_obj (ReportCase): case object
            """
            summary_obj.increment(case_obj.get_status())

        self.status = c.RESULT_SUCCESS
        summary = ReportSummary()
        [increment_summary(summary, case) for case in self.cases]
        if summary.get_failed() > 0:
            self.status = c.RESULT_FAILURE
        self.summary = summary

    def as_json(self):
        """Dump ReportGroup object as simple python dictionary

        The returned dictionary can be easily converted to JSON via 
        'json.dumps', either on its own or as part of a larger object (e.g.
        Report)

        Returns:
            dict: ReportGroup object as python dictionary
        """

        return {
            "phase_name": self.name,
            "phase_description": "",
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
            "summary": self.summary.as_json(),
            "tests": [case.as_json() for case in self.cases]
        }

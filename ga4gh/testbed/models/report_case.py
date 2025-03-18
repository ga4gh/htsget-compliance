# -*- coding: utf-8 -*-
"""Testbed ReportCase, reports on a single compliance test case"""

from ga4gh.testbed import constants as c
from ga4gh.testbed.models.report_summary import ReportSummary

class ReportCase(object):
    """Reports on a single compliance test case

    Attributes:
        name (str): test case name
        status (int): indicates test case success, warning, failure, skip
        debug (list): debug messages produced throughout test
        info (list): info messages produced throughout test
        warn (list): warning messages produced throughout test
        error (str): error message that led to test case failure
    """

    def __init__(self):
        """Instantiates a ReportCase object"""

        self.name = None
        self.status = None
        self.debug = []
        self.info = []
        self.warn = []
        self.error = None
        self.start_time = None
        self.end_time = None
        self.summary = None
        self.cases = []
    
    def set_name(self, name):
        """set name

        Args:
            name (str): name of test case
        """

        self.name = name
    
    def get_name(self):
        """get name

        Returns:
            str: name of test case
        """

        return self.name

    def add_case(self, case_obj):
        """add a Case to the group

        Args:
            case_obj (Case): object to add to group
        """

        self.cases.append(case_obj)
    
    def set_status_success(self):
        """set status to 'successful'"""

        self.status = c.RESULT_SUCCESS

    def set_status_warning(self):
        """set status to 'warning'"""

        self.status = c.RESULT_WARNING

    def set_status_failure(self):
        """set status to 'failure'"""

        self.status = c.RESULT_FAILURE

    def set_status_skipped(self):
        """set status to 'skipped'"""

        self.status = c.RESULT_SKIPPED
    
    def get_status(self):
        """get status

        Returns:
            int: status
        """

        return self.status
    
    def add_debug_msg(self, message):
        """add single message to list of debug messages

        Args:
            message (str): debug message
        """

        self.debug.append(message)
    
    def get_debug(self):
        """get debug message list

        Returns:
            list: debug message list
        """

        return self.debug
    
    def add_info_msg(self, message):
        """add single message to list of info messages

        Args:
            message (str): info message
        """

        self.info.append(message)

    def get_info(self):
        """get info message list

        Returns:
            list: info message list
        """

        return self.info
    
    def add_warn_msg(self, message):
        """add single message to list of warning messages

        Args:
            message (str): warning message
        """

        self.warn.append(message)
    
    def get_warn(self):
        """get warning message list

        Returns:
            list: warning message list
        """

        return self.warn
    
    def set_error(self, message):
        """set error message

        Args:
            message (str): error message
        """

        self.error = message
    
    def get_error(self):
        """get error message

        Returns:
            error message
        """

        return self.error

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

        summary = ReportSummary()
        [increment_summary(summary, case) for case in self.cases]
        self.summary = summary

    def as_json(self):
        """Dump ReportCase object as simple python dictionary

        The returned dictionary can be easily converted to JSON via 
        'json.dumps', either on its own or as part of a larger object (e.g.
        ReportGroup, Report)

        Returns:
            dict: ReportCase object as python dictionary
        """

        return {
            "test_name": self.name,
            "test_description": "Test to check if info-endpoint returns 200 OK with appropriate headers",
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.get_status(),
            "summary": self.summary.as_json(),
            "message": "",
            "cases": [
                {
                    "case_name": self.name,
                    "case_description": "Test to check if info-endpoint returns 200 OK with appropriate headers",
                    "log_messages": [],
                    "start_time": self.start_time,
                    "end_time": self.end_time,
                    "status": self.get_status(),
                    "message": ""
                }
            ]
        }

# -*- coding: utf-8 -*-
"""Testbed ReportCase, reports on a single compliance test case"""

from ga4gh.testbed import constants as c

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
            "summary": {},
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

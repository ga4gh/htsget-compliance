# -*- coding: utf-8 -*-
"""Testbed ReportSummary, summarizes statuses of cases in a group or report"""

from ga4gh.testbed import constants as c

class ReportSummary(object):
    """Summarizes statuses of all cases in a group or report

    Attributes:
        run (int): total number of cases run
        passed (int): total number of cases passed
        warned (int): total number of cases passed with warning(s)
        failed (int): total number of cases failed
        skipped (int): total number of cases skipped
        increment_dict (dict): increments the correct attribute by status code
    """
    
    def __init__(self):
        """Instantiate a ReportSummary"""

        self.run = 0
        self.passed = 0
        self.warned = 0
        self.failed = 0
        self.skipped = 0
        self.increment_dict = {
            c.RESULT_SUCCESS: self.increment_passed,
            c.RESULT_WARNING: self.increment_warned,
            c.RESULT_FAILURE: self.increment_failed,
            c.RESULT_SKIPPED: self.increment_skipped
        }
    
    def increment_run(self):
        """increment run count by 1"""

        self.run += 1
    
    def get_run(self):
        """get run count
        
        Returns:
            int: run count
        """

        return self.run
    
    def increment_passed(self):
        """increment pass count by 1"""

        self.passed += 1
    
    def get_passed(self):
        """get passed count

        Returns:
            int: passed count
        """

        return self.passed
    
    def increment_warned(self):
        """increment warn count by 1"""

        self.warned += 1
    
    def get_warned(self):
        """get warn count

        Returns:
            int: warn count
        """

        return self.warned
    
    def increment_failed(self):
        """increment fail count by 1"""

        self.failed += 1
    
    def increment_skipped(self):
        """increment skip count by 1"""

        self.skipped += 1

    def increment(self, status):
        """increment run and status-specific counts by 1

        For a given status code, increment the total number of cases run, as
        well as the count for that status by 1

        Args:
            status (int): status code to increment
        """

        self.increment_run()
        self.increment_dict[status]()

    def add_from_summary(self, summary_obj):
        """add all counts from another summary to the existing summary

        Used when aggregating summaries from multiple groups for the overall
        report.

        Args:
            summary_obj (ReportSummary): another ReportSummary object
        """

        self.run += summary_obj.run
        self.passed += summary_obj.passed
        self.warned += summary_obj.warned
        self.failed += summary_obj.failed
        self.skipped += summary_obj.skipped

    def as_json(self):
        """Dump ReportSummary as simple python dictionary

        The returned dictionary can be easily converted to JSON via 
        'json.dumps', either on its own or as part of a larger object (e.g.
        ReportGroup, Report)

        Returns:
            dict: ReportSummary object as python dictionary
        """

        return {
            "run": self.run,
            "passed": self.passed,
            "warned": self.warned,
            "failed": self.failed,
            "skipped": self.skipped
        }

import json
from ga4gh.testbed.models.report_summary import ReportSummary

class ReportGroup(object):
    
    def __init__(self):
        self.name = None
        self.summary = None
        self.cases = []

    def add_case(self, case_obj):
        self.cases.append(case_obj)
    
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def summarize(self):

        def increment_summary(summary_obj, case_obj):
            summary_obj.increment(case_obj.get_status())

        summary = ReportSummary()
        [increment_summary(summary, case) for case in self.cases]
        self.summary = summary

    def as_json(self):
        return {
            "name": self.name,
            "summary": self.summary.as_json(),
            "cases": [case.as_json() for case in self.cases]
        }

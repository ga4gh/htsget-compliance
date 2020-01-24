import datetime
import json
from ga4gh.testbed.models.report_summary import ReportSummary

class Report(object):
    
    def __init__(self):
        self.id = None
        self.configuration_id = None
        self.parameters = {}
        self.generated_at = None
        self.summary = None
        self.groups = []

    def set_id(self, uniqid):
        self.id = uniqid
    
    def get_id(self):
        return self.id
    
    def set_configuration_id(self, configuration_id):
        self.configuration_id = configuration_id
    
    def get_configuration_id(self):
        return self.configuration_id
    
    def set_parameters(self, parameters):
        self.parameters = parameters
    
    def get_parameters(self):
        return self.parameters

    def summarize(self):
        summary = ReportSummary()
        [summary.add_from_summary(group.summary) for group in self.groups]
        self.summary = summary

    def add_group(self, group_obj):
        self.groups.append(group_obj)
    
    def finalize(self):
        self.generated_at = str(datetime.datetime.now().isoformat())
        self.summarize()

    def as_json(self):
        return {
            "id": self.get_id(),
            "configurationId": self.get_configuration_id(),
            "parameters": self.get_parameters(),
            "generatedAt": self.generated_at,
            "summary": self.summary.as_json(),
            "groups": [group.as_json() for group in self.groups]
        }
    
    def __str__(self):
        return json.dumps(self.as_json())

from ga4gh.testbed import constants as c

class ReportSummary(object):
    
    def __init__(self):
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
        self.run += 1
    
    def increment_passed(self):
        self.passed += 1
    
    def increment_warned(self):
        self.warned += 1
    
    def increment_failed(self):
        self.failed += 1
    
    def increment_skipped(self):
        self.skipped += 1

    def increment(self, status):
        self.increment_run()
        self.increment_dict[status]()

    def add_from_summary(self, summary_obj):
        self.run += summary_obj.run
        self.passed += summary_obj.passed
        self.warned += summary_obj.warned
        self.failed += summary_obj.failed
        self.skipped += summary_obj.skipped

    def as_json(self):
        return {
            "run": self.run,
            "passed": self.passed,
            "warned": self.warned,
            "failed": self.failed,
            "skipped": self.skipped
        }
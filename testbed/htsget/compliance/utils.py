import datetime
import os

from ga4gh.testbed.report.constants import TIMESTAMP_FORMAT

TEST_SUITE = os.path.dirname(__file__)

# Additional utility functions to load the sequence data

def now():
    return str(datetime.datetime.utcnow().strftime(TIMESTAMP_FORMAT))
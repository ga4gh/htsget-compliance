# -*- coding: utf-8 -*-
"""htsget compliance test cases

Attributes:
    TEST_GROUPS (dict): contains list of test cases by endpoint (reads, 
        variants). If a web service does not implement either API route, the
        corresponding test cases will not be run.
"""

import inspect
import os
from testbed.htsget.compliance.config import constants as c
from testbed.htsget.compliance.config import methods as m
from testbed.htsget.compliance.config import test_case_property_matrix as tcpm

TEST_GROUPS = {
    "reads": {
        "cases": tcpm.construct_reads_test_cases_matrix()
    },
    "variants": {
        "cases": [

        ]
    }
}

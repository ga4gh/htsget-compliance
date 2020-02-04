# -*- coding: utf-8 -*-
"""Unit Tests for ga4gh.testbed.models.report_group module"""

from ga4gh.testbed.models.report_group import ReportGroup
from ga4gh.testbed.models.report_case import ReportCase
from ga4gh.testbed import constants as c

all_group_info = [
    {
        "name": "reads",
        "cases": [
            {
                "name": "get reads 1",
                "status": c.RESULT_SUCCESS
            },
            {
                "name": "get reads 2",
                "status": c.RESULT_SKIPPED
            },
            {
                "name": "get reads 3",
                "status": c.RESULT_SUCCESS
            }
        ]
    },
    {
        "name": "sequence",
        "cases": [
            {
                "name": "get sequence 1",
                "status": c.RESULT_WARNING
            },
            {
                "name": "get sequence 2",
                "status": c.RESULT_WARNING
            },
            {
                "name": "get sequence 3",
                "status": c.RESULT_WARNING
            }
        ]
    },
    {
        "name": "expressions",
        "cases": [
            {
                "name": "get expression 1",
                "status": c.RESULT_FAILURE
            },
            {
                "name": "get expression 2",
                "status": c.RESULT_SKIPPED
            },
            {
                "name": "get expression 3",
                "status": c.RESULT_FAILURE
            }
        ]
    }

]

def set_case_status(case, status):
    """sets case status according to status int

    Args:
        case (ReportCase): ReportCase object to set status
        status (int): pass/warn/fail/skip status int
    """

    set_status = {
        c.RESULT_SUCCESS: case.set_status_success,
        c.RESULT_WARNING: case.set_status_warning,
        c.RESULT_FAILURE: case.set_status_failure,
        c.RESULT_SKIPPED: case.set_status_skipped
    }

    set_status[status]()

def test_add_case():
    """pytest: test add_case method"""

    for group_info in all_group_info:
        group = ReportGroup()
        for case_info in group_info["cases"]:
            case = ReportCase()
            case.set_name(case_info["name"])
            set_case_status(case, case_info["status"])
            group.add_case(case)
        assert len(group.cases) == len(group_info["cases"])
        assert group.cases[0].get_name() == group_info["cases"][0]["name"]
        assert group.cases[0].get_status() == group_info["cases"][0]["status"]

def test_name():
    """pytest: test set/get name"""

    for group_info in all_group_info:
        group = ReportGroup()
        group.set_name(group_info["name"])
        assert group.get_name() == group_info["name"]

def test_summarize():
    """pytest: test summarize method"""

    



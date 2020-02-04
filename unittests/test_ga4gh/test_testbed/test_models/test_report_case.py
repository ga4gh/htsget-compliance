# -*- coding: utf-8 -*-
"""Unit Tests for ga4gh.testbed.models.report_case module"""

from ga4gh.testbed.models.report_case import ReportCase
from ga4gh.testbed import constants as c

data = [
    {
        "name": "test case a",
        "status": c.RESULT_FAILURE,
        "debug": [
            "first debug message",
            "second debug message"
        ],
        "error": "an error occurred"
    },
    {
        "name": "htsget test case",
        "status": c.RESULT_SUCCESS,
        "info": [
            "first info message",
            "second info message"
        ]
    },
    {
        "name": "test refget service",
        "status": c.RESULT_WARNING,
        "warn": [
            "first warning message",
            "second warning message"
        ]
    }
]

def test_name():
    """pytest: test set/get name"""

    case = ReportCase()
    for case_info in data:
        case.set_name(case_info["name"])
        assert case.get_name() == case_info["name"]

def test_status():
    """pytest: test set/get status"""

    case = ReportCase()
    assert case.get_status() == None
    case.set_status_success()
    assert case.get_status() == c.RESULT_SUCCESS
    case.set_status_warning()
    assert case.get_status() == c.RESULT_WARNING
    case.set_status_failure()
    assert case.get_status() == c.RESULT_FAILURE
    case.set_status_skipped()
    assert case.get_status() == c.RESULT_SKIPPED

def test_messages():
    """pytest: test set/get different log level messages"""

    for case_info in data:
        case = ReportCase()

        keys = ["debug", "info", "warn"]
        add = {
            "debug": case.add_debug_msg,
            "info": case.add_info_msg,
            "warn": case.add_warn_msg
        }
        get = {
            "debug": case.get_debug,
            "info": case.get_info,
            "warn": case.get_warn
        }

        for key in ["debug", "info", "warn"]:
            if key in case_info.keys():
                for msg in case_info[key]:
                    add[key](msg)
                logs = get[key]()
                assert len(logs) == len(case_info[key])
                assert logs[0] == case_info[key][0]
        
        if "error" in case_info.keys():
            case.set_error(case_info["error"])
            assert case.get_error() == case_info["error"]

def test_as_json():
    """pytest: test as_json method"""

    for case_info in data:
        case = ReportCase()
        case.set_name(case_info["name"])
        set_status = {
            c.RESULT_SUCCESS: case.set_status_success,
            c.RESULT_WARNING: case.set_status_warning,
            c.RESULT_FAILURE: case.set_status_failure,
            c.RESULT_SKIPPED: case.set_status_skipped
        }
        add = {
            "debug": case.add_debug_msg,
            "info": case.add_info_msg,
            "warn": case.add_warn_msg
        }

        set_status[case_info["status"]]()

        for key in ["debug", "info", "warn"]:
            if key in case_info.keys():
                for msg in case_info[key]:
                    add[key](msg)

        if "error" in case_info.keys():
            case.set_error(case_info["error"])
        
        json = case.as_json()
        assert json["name"] == case_info["name"]
        assert json["status"] == case_info["status"]

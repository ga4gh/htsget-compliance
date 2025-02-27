# -*- coding: utf-8 -*-
"""Unit Tests for ga4gh.testbed.models.report_summary module

Attributes:
    status_ints (dict): maps status strings to associated ints
    counts (dict): sample status counts for multiple report summary objects
"""

from testbed.testbed.models.report_summary import ReportSummary
from ga4gh.testbed import constants as c

status_ints = {
    "passed": c.RESULT_SUCCESS,
    "warned": c.RESULT_WARNING,
    "failed": c.RESULT_FAILURE,
    "skipped": c.RESULT_SKIPPED
}

counts = {
    "a": {
        "passed": 2,
        "warned": 5,
        "failed": 6,
        "skipped": 1
    },
    "b": {
        "passed": 1,
        "warned": 3,
        "failed": 7,
        "skipped": 4
    },
    "c": {
        "passed": 9,
        "warned": 6,
        "failed": 3,
        "skipped": 2
    }
}

def generate_report_summary_dict():
    """populate summary objects with sample status counts
    
    Returns:
        dict: ReportSummary objects populated with test status counts
    """

    summaries = {
        "a": ReportSummary(),
        "b": ReportSummary(),
        "c": ReportSummary()
    }

    for l in ["a", "b", "c"]:
        summary = summaries[l]
        for status_string in ["passed", "warned", "failed", "skipped"]:
            status_int = status_ints[status_string]
            count = counts[l][status_string]
            for i in range(0, count):
                summary.increment(status_int)
    
    return summaries

def test_increment_run():
    """pytest: test increment_run method"""

    summary = ReportSummary()
    assert summary.get_run() == 0
    summary.increment_run()
    assert summary.get_run() == 1
    summary.increment_run()
    assert summary.get_run() == 2

def test_increment_passed():
    """pytest: test increment_passed method"""

    summary = ReportSummary()
    assert summary.get_passed() == 0
    summary.increment_passed()
    assert summary.get_passed() == 1
    for i in range(0, 9):
        summary.increment_passed()
    assert summary.get_passed() == 10

def test_increment_warned():
    """pytest: test increment_warned method"""

    summary = ReportSummary()
    assert summary.get_warned() == 0
    summary.increment_warned()
    assert summary.get_warned() == 1
    for i in range(0, 20):
        summary.increment_warned()
    assert summary.get_warned() == 21

def test_increment_failed():
    """pytest: test increment_failed method"""

    summary = ReportSummary()
    assert summary.get_failed() == 0
    summary.increment_failed()
    assert summary.get_failed() == 1
    for i in range(0, 35):
        summary.increment_failed()
    assert summary.get_failed() == 36

def test_increment_skipped():
    """pytest: test increment_skipped method"""

    summary = ReportSummary()
    assert summary.get_skipped() == 0
    summary.increment_skipped()
    assert summary.get_skipped() == 1
    for i in range(0, 99):
        summary.increment_skipped()
    assert summary.get_skipped() == 100

def test_increment():
    """pytest: test increment method"""

    summary = ReportSummary()
    summary.increment(c.RESULT_SUCCESS)
    assert summary.get_passed() == 1
    assert summary.get_run() == 1
    summary.increment(c.RESULT_FAILURE)
    assert summary.get_failed() == 1
    assert summary.get_run() == 2
    summary.increment(c.RESULT_WARNING)
    assert summary.get_warned() == 1
    assert summary.get_run() == 3
    summary.increment(c.RESULT_SKIPPED)
    assert summary.get_skipped() == 1
    assert summary.get_run() == 4

def test_add_from_summary():
    """pytest: test add_from_summary method"""

    summaries = generate_report_summary_dict()
    summaries["a"].add_from_summary(summaries["b"])
    assert summaries["a"].get_passed() == 3
    assert summaries["a"].get_warned() == 8
    assert summaries["a"].get_failed() == 13
    assert summaries["a"].get_skipped() == 5
    assert summaries["a"].get_run() == 29

    summaries["a"].add_from_summary(summaries["c"])
    assert summaries["a"].get_passed() == 12
    assert summaries["a"].get_warned() == 14
    assert summaries["a"].get_failed() == 16
    assert summaries["a"].get_skipped() == 7
    assert summaries["a"].get_run() == 49

def test_as_json():
    """pytest: test as_json method"""

    summaries = generate_report_summary_dict()
    for l in ["a", "b", "c"]:
        summary = summaries[l]
        json = summary.as_json()
        assert json["passed"] == counts[l]["passed"]
        assert json["warned"] == counts[l]["warned"]
        assert json["failed"] == counts[l]["failed"]
        assert json["skipped"] == counts[l]["skipped"]

# -*- coding: utf-8 -*-
"""Unit Tests for ga4gh.testbed.models.report_summary module"""

from ga4gh.testbed.models.report_summary import ReportSummary

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

from asyncio.windows_events import NULL
import requests

from testbed.htsget.compliance.utils import now

case_start_time = {}
case_end_time = {}

def demo_test(test, runner):
    test.description = "demo test for development"
    base_url = str(runner.base_url)
    response = requests.get(base_url)
    if response.status_code ==200:
        test.result = 1
    else:
        test.result = -1

def get_test_start_times():
    return case_start_time

def get_test_end_times():
    return case_end_time


tests_in_phase = {'phase1': [], 'phase2': [], 'phase3': [], 'phase4': []}

def initiate_tests():
    '''
    Initiates test case objects and generates a test case graph for execution
    '''

    def base_algorithm(test, runner):
        if True is True:
            test.result = 1


    return NULL
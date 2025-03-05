import requests
import sys
from testbed.htsget.compliance.utils import now
from testbed.htsget.compliance.config.tests import TEST_GROUPS

case_start_time = {}
case_end_time = {}

class Test():
    def __init__(self, algorithm):
        '''
        Initiates the Test Case object. Algorithm is a required field to initiate test case object
        '''
        self.label = 0
        self.algorithm = algorithm
        self.result = 2
        self.pass_text = ''
        self.fail_text = ''
        self.skip_text = ''
        self.parents = []
        self.children = []
        self.warning = False
        self.cases = []
        self.case_outputs = []
        self.phase = ''
        self.response_body = ''
        self.description = ''

    def __str__(self):
        '''
        String repr of the test case
        '''
        return 'test_' + self.algorithm.__name__

    def set_pass_text(self, text):
        '''
        Setter for pass_text
        '''
        self.pass_text = text

    def set_fail_text(self, text):
        '''
        Setter for fail_text
        '''
        self.fail_text = text

    def set_skip_text(self, text):
        '''
        Setter for skip_text
        '''
        self.skip_text = text

    def generate_skip_text(self):
        '''
        Skip text is generated if there is no skip text (the case when test is skipped when the parent test cases fail or skip)
        To track down the root cause of this skip.
        '''
        text = str(self) + ' is skipped because '
        for test in self.parents:
            if test.result != 1:
                text = text + test.to_echo()
        return text

    def add_parent(self, parent_test_case):
        '''
        Adds a parent test case
        '''
        self.parents.append(parent_test_case)

    def add_child(self, child_test_case):
        '''
        Adds a child test case
        '''
        self.children.append(child_test_case)
        child_test_case.add_parent(self)

    def to_skip(self):
        '''
        Checks if any of the parent test cases failed or skipped which causes this case to skip
        '''
        for test in self.parents:
            if test.result != 1:
                print("{} - {}".format(str(test), str(test.result)), file=sys.stderr)
                return True
        return False

    def run(self, test_runner):
        '''
        First checks if the parent test cases were successful then run the text.
        '''
        print(str(self), file=sys.stderr)
        # Checking if to skip
        if self.to_skip() is True:
            # warning will be generated because the test case is skipped because of some parent failure
            self.warning = True
            self.result = 0
            return
        # run the test if not skipped
        self.algorithm(self, test_runner)
        # if it fails it'll generate a warning
        if self.result == -1:
            self.warning = True
        if self.result not in (0, 1):
            print(str(self), self.to_echo(), file=sys.stderr)

    def to_echo(self):
        '''
        Returns the text based on the result of the test case
        '''
        if self.result == 1:
            return self.pass_text
        elif self.result == -1:
            return self.fail_text
        elif self.result == 2:
            return 'Unknown error'
        elif self.skip_text == '':
            self.skip_text = self.generate_skip_text()
        return self.skip_text

    def set_phase(self, phase):
        self.phase = phase

    def get_phase(self):
        return self.phase


def get_test_start_times():
    return case_start_time

def get_test_end_times():
    return case_end_time


tests_in_phase = {'reads': TEST_GROUPS["reads"]["cases"], 'variants': TEST_GROUPS["variants"]["cases"]}

def initiate_tests():
    '''
    Initiates test case objects and generates a test case graph for execution
    '''

    def base_algorithm(test, runner):
        if True is True:
            test.result = 1

    for phase in tests_in_phase:
        print(tests_in_phase[phase])        
        #test_reads = Test()
        #test_reads = 



    # reads_test_cases = construct_reads_test_cases_matrix()

    test_base = Test(base_algorithm)

    # File Validator Test Cases
    # test_reads = Test()

    # test_info_implement = Test(info_implement)
    # test_info_implement.set_phase('service info')
    # test_info_implement.set_pass_text('Info endpoint implemented by the server')
    # test_info_implement.set_fail_text('Info endpoint not implemented by the server')

    # test_info_implement = Test(info_implement)
    # test_info_implement.set_phase('service info')
    # test_info_implement.set_pass_text('Info endpoint implemented by the server')
    # test_info_implement.set_fail_text('Info endpoint not implemented by the server')

    # test_info_implement = Test(info_implement)
    # test_info_implement.set_phase('service info')
    # test_info_implement.set_pass_text('Info endpoint implemented by the server')
    # test_info_implement.set_fail_text('Info endpoint not implemented by the server')

    # tests_in_phase['service info'] = ['test_info_implement',
    #                                   'test_info_implement_default']

    # for endpoint in c.ENDPOINTS:
    #     group = ReportGroup()
    #     group.set_name(endpoint)
    #     cases = TEST_GROUPS[endpoint]["cases"]
    #     for case_props in cases:
    #         test_case_obj = TestCase(case_props, kwargs)
    #         report_case = test_case_obj.execute_test()
    #         group.add_case(report_case)
    #     group.summarize()
    #     report.add_group(group)

    #return test_base



# Test Cases
def demo_test(test, runner):
    test.description = "demo test for development"
    base_url = str(runner.base_url)
    response = requests.get(base_url)
    if response.status_code ==200:
        test.result = 1
    else:
        test.result = -1
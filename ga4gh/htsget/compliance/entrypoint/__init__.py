import click
import datetime
import json
import requests
import uuid
from ga4gh.htsget.compliance.config.tests import TEST_GROUPS
from ga4gh.htsget.compliance.config import constants as c
from ga4gh.htsget.compliance.methods.test_api_response import test_api_response

@click.command()
@click.argument("htsget_url")
@click.argument("orchestrator_url")
def main(**kwargs):

    for endpoint in c.ENDPOINTS:
        cases = TEST_GROUPS[endpoint]["cases"]
        for case in cases:
            test_api_response(case, kwargs)


    """
    configuration_id = "5e27341e58496513e01c6510"
    report = {
        "id": str(uuid.uuid1()),
        "configurationId": configuration_id,
        "parameters": {},
        "generatedAt": str(datetime.datetime.now().isoformat()),
        "summary": {
            "run": 5,
            "passed": 2,
            "warned": 1,
            "failed": 2,
            "skipped": 0
        },
        "groups": [
            {
                "name": "Reads",
                "summary": {
                    "run": 3,
                    "passed": 1,
                    "warned": 1,
                    "failed": 1,
                    "skipped": 0
                },
                "cases": [
                    {
                        "name": "Get test BAM",
                        "status": 1
                    },
                    {
                        "name": "Get test CRAM",
                        "status": 2
                    },
                    {
                        "name": "Get test SAM",
                        "status": 3
                    }
                ]
            },
            {
                "name": "Variants",
                "summary": {
                    "run": 2,
                    "passed": 1,
                    "warned": 0,
                    "failed": 1,
                    "skipped": 0
                },
                "cases": [
                    {
                        "name": "Get test VCF",
                        "status": 1
                    },
                    {
                        "name": "Get test BCF",
                        "status": 3
                    }
                ]
            }
        ]
    }

    response = requests.post(
        kwargs["orchestrator_url"],
        json=report
    )

    print(response.content)
    """

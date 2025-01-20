# -*- coding: utf-8 -*-
"""Unit Tests for ga4gh.htsget.compliance.schema_validator module

Tests that certain responses reliably succeed or fail validation when expected

Attributes:
    INSTANCE_SUCCESS_0 (dict): valid response
    INSTANCE_SUCCESS_1 (dict): valid response
    INSTANCE_FAIL_0 (dict): invalid response (empty object)
    INSTANCE_FAIL_1 (dict): invalid response (incorrect format)
    INSTANCE_FAIL_2 (dict): invalid response (missing url property)
    INSTANCE_FAIL_3 (dict): invalid response (incorrect class)
    INSTANCE_SUCCESSES (list): all valid responses
    INSTANCE_FAILURES (list): all invalid responses
"""

from ga4gh.htsget.compliance.schema_validator import SchemaValidator

INSTANCE_SUCCESS_0 = {
    "htsget": {
        "format": "BAM",
        "urls": [
            {
                "url": "https://htsget.ga4gh-demo.org/file.bam"
            }
        ]
    }
}

INSTANCE_SUCCESS_1 = {
    "htsget": {
        "format": "CRAM",
        "urls": [
            {
                "url": "https://htsget.ga4gh-demo.org/header.bam",
                "headers": {
                    "Authorization": "Bearer abcdef"
                },
                "class": "header"
            },
            {
                "url": "https://htsget.ga4gh-demo.org/body.bam",
                "headers": {
                    "Authorization": "Beader abcdef"
                },
                "class": "body"
            }
        ]
    }
}

INSTANCE_FAIL_0 = {}

INSTANCE_FAIL_1 = {
    "htsget": {
        "format": "MPEG-G",
        "urls": [
            {
                "url": "https://htsget.ga4gh-demo.org/header.bam",
                "headers": {
                    "Authorization": "Bearer abcdef"
                },
                "class": "header"
            }
        ]
    }
}

INSTANCE_FAIL_2 = {
    "htsget": {
        "format": "CRAM",
        "urls": [
            {
                "headers": {
                    "Authorization": "Bearer abcdef"
                },
                "class": "header"
            }
        ]
    }
}

INSTANCE_FAIL_3 = {
    "htsget": {
        "format": "CRAM",
        "urls": [
            {
                "url": "https://htsget.ga4gh-demo.org/footer.bam",
                "headers": {
                    "Authorization": "Bearer abcdef"
                },
                "class": "footer"
            },
            {
                "url": "https://htsget.ga4gh-demo.org/body.bam",
                "headers": {
                    "Authorization": "Beader abcdef"
                },
                "class": "body"
            }
        ]
    }
}

INSTANCE_SUCCESSES = [
    INSTANCE_SUCCESS_0,
    INSTANCE_SUCCESS_1
]

INSTANCE_FAILURES = [
    INSTANCE_FAIL_0,
    INSTANCE_FAIL_1,
    INSTANCE_FAIL_2,
    INSTANCE_FAIL_3
]

def test_schema_validator():
    """pytest: test SchemaValidator class"""

    def get_validation_result(instance_json):
        """Get SchemaValidator validation result

        Args:
            instance_json (dict): test json object

        Returns:
            dict: JSON schema validation result
        """

        sv = SchemaValidator()
        return sv.validate_instance(instance_json)

    for instance in INSTANCE_SUCCESSES:
        result = get_validation_result(instance)
        assert result["status"] == SchemaValidator.SUCCESS
    
    for instance in INSTANCE_FAILURES:
        result = get_validation_result(instance)
        assert result["status"] == SchemaValidator.FAILURE

# -*- coding: utf-8 -*-
"""Constants related to htsget compliance

Attributes:
    STATUS_OK (int): HTTP "OK" response code
    STATUS_NOT_FOUND (int): HTTP "NOT FOUND" response code
    SCHEMA_HTSGET_URL (str): filename for htsgetUrl JSON schema
    SCHEMA_HTSGET_RESPONSE (str): filename for htsgetResponse JSON schema
    ENDPOINTS (list): endpoints prescribed by the htsget specification
    BASE_URL (str): unformatted url template
    DEFAULT_READS_URLPATH (str): unformmated url template for reads-related
        requests
    DEFAULT_VARIANTS_URLPATH (str): unformated url template for variants-related
        requests
    READS_ID_FOUND_1 (str): id for test case(s)
    READS_ID_FOUND_2 (str): id for test case(s)
    READS_ID_NOTFOUND_1 (str): id for test case(s)
    READS_ID_NOTFOUND_2 (str): id for test case(s)
"""

import inspect
import os

# HTTP STATUS CODES
STATUS_OK = 200
STATUS_NOT_FOUND = 404

# SCHEMA FILENAMES
SCHEMA_HTSGET_URL = "htsgetUrl.json"
SCHEMA_HTSGET_RESPONSE = "htsgetResponse.json"

# ENDPOINTS
ENDPOINTS = ["reads", "variants"]

# URL TEMPLATES
BASE_URL = "{base_url}"
DEFAULT_READS_URLPATH = BASE_URL + "/reads"
DEFAULT_VARIANTS_URLPATH = BASE_URL + "/variants"
ID_URLPATH = "/{obj_id}"

# OBJECT IDs FOR TEST CASES
READS_ID_FOUND_1 = "NA30000M"
READS_ID_FOUND_2 = "10X_P4_0_possorted_genome.bam"
READS_ID_NOTFOUND_1 = "notfound123456789"
READS_ID_NOTFOUND_2 = "notfound987654321"

# FILE FORMAT REQUEST PARAMETERS AND EXTENSIONS
FORMAT_SAM = "SAM"
FORMAT_BAM = "BAM"
FORMAT_CRAM = "CRAM"
EXTENSION_SAM = ".sam"
EXTENSION_BAM = ".bam"
EXTENSION_CRAM = ".cram"

# REFERENCE NAMES
REFERENCE_PHIX = "phix"

DATA_DIR = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    ),
    "data"
)

# -*- coding: utf-8 -*-
"""Constants related to htsget compliance

Attributes:
    STATUS_OK (int): HTTP "OK" response code
    STATUS_NOT_FOUND (int): HTTP "NOT FOUND" response code
    SCHEMA_HTSGET_URL (str): filename for htsgetUrl JSON schema
    SCHEMA_HTSGET_RESPONSE (str): filename for htsgetResponse JSON schema
    ENDPOINTS (list): endpoints prescribed by the htsget specification
    BASE_URL (str): unformatted url template
    READS_URL (str): unformmated url template for reads-related requests
    VARIANTS_URL (str): unformated url template for variants-related requests
    READS_ID_FOUND_1 (str): id for test case(s)
    READS_ID_FOUND_2 (str): id for test case(s)
    READS_ID_NOTFOUND_1 (str): id for test case(s)
    READS_ID_NOTFOUND_2 (str): id for test case(s)
"""

# HTTP STATUS CODES
STATUS_OK = 200
STATUS_NOT_FOUND = 404

# SCHEMA FILENAMES
SCHEMA_HTSGET_URL = "htsgetUrl.json"
SCHEMA_HTSGET_RESPONSE = "htsgetResponse.json"

# ENDPOINTS
ENDPOINTS = ["reads", "variants"]

# URL TEMPLATES
BASE_URL = "{base_url}/"
READS_URL = BASE_URL + "reads/{obj_id}"
VARIANTS_URL = BASE_URL + "variants/{obj_id}"

# OBJECT IDs FOR TEST CASES
READS_ID_FOUND_1 = "10X_P4_0_possorted_genome.bam"
READS_ID_FOUND_2 = "10X_P4_0_possorted_genome.bam"
READS_ID_NOTFOUND_1 = "notfound123456789"
READS_ID_NOTFOUND_2 = "notfound987654321"

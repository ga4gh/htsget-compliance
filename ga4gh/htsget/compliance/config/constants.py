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
DEFAULT_READS_URLPATH = "/reads"
DEFAULT_VARIANTS_URLPATH = "/variants"
ID_URLPATH = "/{obj_id}"

# OBJECT IDs FOR TEST CASES
READS_ID_FOUND_1 = "htsnexus_test_NA12878"
READS_ID_FOUND_2 = "htsnexus_test_NA12878.bam"
READS_ID_NOTFOUND_1 = "notfound123456789"
READS_ID_NOTFOUND_2 = "notfound987654321"

VARIANTS_ID_FOUND_1 = "spec-v4.3"
VARIANTS_ID_FOUND_2 = "spec-v4.3.vcf.gz"
VARIANTS_ID_NOTFOUND_1 = "notfoundmeowmeow"
VARIANTS_ID_NOTFOUND_1 = "notfoundfoobarbaz"

## Crypt4GH
PUBLIC_KEY_CRYPT4GH = "alice.pub"
PRIVATE_KEY_CRYPT4GH = "bob.sec"
EXTENSION_C4GH = ".c4gh"

# FILE FORMAT REQUEST PARAMETERS AND EXTENSIONS
FORMAT_BAM = "BAM"
FORMAT_CRAM = "CRAM"
FORMAT_VCF = "VCF"
FORMAT_BCF = "BCF"
EXTENSION_BAM = ".bam"
EXTENSION_CRAM = ".cram"
EXTENSION_VCF = ".vcf.gz" # We'll assume that's the de-facto standard in 2025 (vs uncompressed .vcf)
EXTENSION_BCF = ".bcf"

# REFERENCE NAMES
REFERENCE_PHIX = "phix"
REFERENCE_HG19 = "hg19"
REFERENCE_CHROM = "11"

# ENCRYPTION SCHEMES
ENCRYPTION_SCHEME_CRYPT4GH = "c4gh"  # Specification available at: https://samtools.github.io/hts-specs/crypt4gh.pdf

DATA_DIR = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    ),
    "data"
)

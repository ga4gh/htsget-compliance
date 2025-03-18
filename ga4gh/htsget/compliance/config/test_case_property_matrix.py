import os
from ga4gh.htsget.compliance.config import constants as c
from ga4gh.htsget.compliance.config import methods

# FIXME: Unnecessary duplication of code in reads/variants test_cases_matrix functions. Refactor.

encryption_schemes = [
    None,
    c.ENCRYPTION_SCHEME_CRYPT4GH,
]

def construct_reads_test_cases_matrix():

    def add_format_param(params, value):
        if value:
            params["format"] = value
    
    def add_reference_name_param(params, value):
        if value:
            params["referenceName"] = value

    def add_encryption_scheme_param(params, value):
        if value:
            params["encryptionScheme"] = value

    def construct_expected_contents_path(reads_id, reads_reference):
        filename = reads_id
        if reads_reference:
            filename += "." + reads_reference
        filepath = os.path.join(c.DATA_DIR, "reads", filename)
        return filepath

    def construct_expected_key_path():
        return os.path.join(c.DATA_DIR, "c4gh", "keys", c.PRIVATE_KEY_CRYPT4GH)
    
    def construct_name(reads_id, reads_format, reads_reference):
        name = "reads: " + reads_id
        if reads_format:
            name += " - " + reads_format
        if reads_reference:
            name += " - " + reads_reference
        return name

    reads = [
        (None, c.READS_ID_FOUND_1, c.READS_ID_FILE_BAM),
        (c.FORMAT_BAM, c.READS_ID_FOUND_1, c.READS_ID_FILE_BAM),
        (c.FORMAT_CRAM, c.READS_ID_FOUND_1, c.READS_ID_FILE_CRAM)
    ]

    # reads_references = [
    #     #None,
    #     #c.REFERENCE_PHIX,
    #     #c.REFERENCE_HG19,
    #     c.REFERENCE_CHROM,
    # ]

    reads_cases = []

    for (reads_format, reads_id, reads_file) in reads:
        for encryption_scheme in encryption_schemes:
            params = {}
            add_format_param(params, reads_format)
            #add_reference_name_param(params, '') #reads_reference)
            if encryption_scheme is not None:
                add_encryption_scheme_param(params, encryption_scheme)

            props = {
                "name": construct_name(
                    reads_id, reads_format, ''#, reads_reference
                ),
                "url_function": methods.FORMAT_READS_URL,
                "url_params": params,
                "obj_id": reads_id,
                "expected_response_status": c.STATUS_OK,
                "expected_contents": construct_expected_contents_path(
                    reads_file, ''),#, reads_reference)
                "expected_key": construct_expected_key_path(),
            }

            reads_cases.append(props)
    
    return reads_cases

def construct_variants_test_cases_matrix():

    def add_format_param(params, value):
        if value:
            params["format"] = value
    
    def add_reference_name_param(params, value):
        if value:
            params["referenceName"] = value

    def add_encryption_scheme_param(params, value):
        if value:
            params["encryptionScheme"] = value

    def construct_expected_contents_path(variants_id, variants_reference):
        filename = variants_id
        if variants_reference:
            filename += "." + variants_reference
        filepath = os.path.join(c.DATA_DIR, "variants", filename)
        return filepath

    def construct_expected_key_path():
        return os.path.join(c.DATA_DIR, "c4gh", "keys", c.PRIVATE_KEY_CRYPT4GH)

    def construct_name(variants_id, variants_format, variants_reference):
        name = "variants: " + variants_id
        if variants_format:
            name += " - " + variants_format
        if variants_reference:
            name += " - " + variants_reference
        return name

    variants = [
        (None, c.VARIANTS_ID_FOUND_1, c.VARIANTS_ID_FILE_VCF),
        (c.FORMAT_VCF, c.VARIANTS_ID_FOUND_1, c.VARIANTS_ID_FILE_VCF),
        (c.FORMAT_BCF, c.VARIANTS_ID_FOUND_1, c.VARIANTS_ID_FILE_BCF)
    ]

    # variants_references = [
    #     None,
    #     c.REFERENCE_CHROM
    # ]

    variants_cases = []

    for (variants_format, variants_id, variants_file) in variants:
        for encryption_scheme in encryption_schemes:
            params = {}
            add_format_param(params, variants_format)
            #add_reference_name_param(params, '') #variants_reference)
            if encryption_scheme is not None:
                add_encryption_scheme_param(params, encryption_scheme)

            props = {
                "name": construct_name(
                    variants_id, variants_format, ''#, variants_reference
                ),
                "url_function": methods.FORMAT_VARIANTS_URL,
                "url_params": params,
                "obj_id": variants_id,
                "expected_response_status": c.STATUS_OK,
                "expected_contents": construct_expected_contents_path(
                    variants_file, ''),#, variants_reference)
                "expected_key": construct_expected_key_path(),
            }

            variants_cases.append(props)
    
    return variants_cases

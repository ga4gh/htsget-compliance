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
    
    def construct_name(reads_id, reads_format, reads_reference):
        name = "reads: " + reads_id
        if reads_format:
            name += " - " + reads_format
        if reads_reference:
            name += " - " + reads_reference
        return name

    reads_ids = [
        c.READS_ID_FOUND_1
    ]

    reads_formats = [
        None,
        c.FORMAT_BAM,
        c.FORMAT_CRAM,
    ]

    reads_references = [
        None,
        #c.REFERENCE_PHIX,
        #c.REFERENCE_HG19,
        c.REFERENCE_CHROM,
    ]

    reads_cases = []

    for reads_id in reads_ids:
        for reads_format in reads_formats:
            for reads_reference in reads_references:
                for encryption_scheme in encryption_schemes:
                    params = {}
                    add_format_param(params, reads_format)
                    add_reference_name_param(params, '') #reads_reference)
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
                            reads_id, '')#, reads_reference)
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
    
    def construct_name(variants_id, variants_format, variants_reference):
        name = "variants: " + variants_id
        if variants_format:
            name += " - " + variants_format
        if variants_reference:
            name += " - " + variants_reference
        return name

    variants_ids = [
        c.VARIANTS_ID_FOUND_1
    ]

    variants_formats = [
        None,
        c.FORMAT_VCF,
        c.FORMAT_BCF
    ]

    variants_references = [
        None,
        c.REFERENCE_CHROM
    ]

    variants_cases = []

    for variants_id in variants_ids:
        for variants_format in variants_formats:
            for variants_reference in variants_references:
                for encryption_scheme in encryption_schemes:
                    params = {}
                    add_format_param(params, variants_format)
                    add_reference_name_param(params, '') #variants_reference)
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
                            variants_id, '')#, variants_reference)
                    }

                    variants_cases.append(props)
    
    return variants_cases

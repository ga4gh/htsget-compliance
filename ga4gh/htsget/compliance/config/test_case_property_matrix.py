import os
from ga4gh.htsget.compliance.config import constants as c
from ga4gh.htsget.compliance.config import methods

def construct_reads_test_cases_matrix():

    def add_format_param(params, value):
        if value:
            params["format"] = value
    
    def add_reference_name_param(params, value):
        if value:
            params["referenceName"] = value

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
        c.FORMAT_CRAM
    ]

    reads_references = [
        None,
        #c.REFERENCE_PHIX
        #c.REFERENCE_HG19
        c.REFERENCE_CHROM
    ]

    reads_cases = []

    for reads_id in reads_ids:
        for reads_format in reads_formats:
            for reads_reference in reads_references:
                params = {}
                add_format_param(params, reads_format)
                add_reference_name_param(params, '') #reads_reference)

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

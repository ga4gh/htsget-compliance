# -*- coding: utf-8 -*-
"""static methods"""

from ga4gh.htsget.compliance.config import constants as c

def format_url(test_case, kwargs, use_reads=True):

    datatype_urlpath = kwargs["reads_base_path"] \
                       if use_reads \
                       else kwargs["variants_base_path"]

    template = c.BASE_URL + datatype_urlpath + c.ID_URLPATH
    url = template.format(**{
        "base_url": kwargs["htsget_url"],
        "obj_id": test_case["obj_id"]
    })

    return url
    
def format_reads_url(test_case, kwargs):
    return format_url(test_case, kwargs)

def format_variants_url(test_case, kwargs):
    return format_url(test_case, kwargs, use_reads=False)

FORMAT_READS_URL = format_reads_url
FORMAT_VARIANTS_URL = format_variants_url

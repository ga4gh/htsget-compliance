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

def get_urls_concatenate_output(url: str, params) -> (bytes, list):
    ''' Fetches and concatenates the payload htsget "urls" array with
        multiple urls where some of those urls contain base64-encoded
        data.

        returns: Tuple with concatenated payload and a list of return codes.
    '''
    response = requests.get(url, params=params)
    data = response.json()

    urls = data.get("htsget", {}).get("urls", [])
    concatenated_data = b""
    status_codes = []

    # First response will be the "top level" htsget request itself
    status_codes.append(response)

    for entry in urls:
        file_url = entry.get("url")
        if file_url.startswith(("http://", "https://")):
            file_response = requests.get(file_url, params=params)
            concatenated_data += file_response.content
            status_codes.append(file_response.status_code)
        elif file_url.startswith("data:;base64,"):
            base64_data = file_url.split("data:;base64,")[-1]
            concatenated_data += base64.b64decode(base64_data)
            status_codes.append(200)  # Assume success for data URIs

    return concatenated_data, status_codes

FORMAT_READS_URL = format_reads_url
FORMAT_VARIANTS_URL = format_variants_url

# -*- coding: utf-8 -*-

import base64
import requests
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

        returns: Tuple with concatenated payload and a list of all responses from all URLs,
                 including embedded data:;<base64> urls.
    '''
    # Toplevel htsget endpoint query, does not need headers for ranges
    try:
        response = requests.get(url, params=params)
    except:
        raise Exception("Perhaps more data:; stuff?")
    data = response.json()

    urls = data.get("htsget", {}).get("urls", [])
    concatenated_data = b""
    all_responses = []

    # First response will be the "top level" htsget request itself
    all_responses.append(response)

    for entry in urls:
        url = entry.get("url")
        if url.startswith(("http://", "https://")):
            headers = entry.get("headers", {})
            response = requests.get(url, headers=headers, params=params)
            # if not (200 <= response.status_code <= 308):
            #     raise Exception(f"Failed to fetch {url}: {response.status_code}")
            concatenated_data += response.content
            all_responses.append(response)
        elif url.startswith("data:;base64,"):
            base64_data = url.split("data:;base64,")[-1]
            concatenated_data += base64.b64decode(base64_data)
            # Assume success for data URIs
            phony_response = requests.Response
            phony_response.status_code=200
            all_responses.append(phony_response)

    return concatenated_data, all_responses

FORMAT_READS_URL = format_reads_url
FORMAT_VARIANTS_URL = format_variants_url

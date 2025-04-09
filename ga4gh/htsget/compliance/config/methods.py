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

def fetch_inline_data(url: str) -> (bytes, object):
    base64_data = url.split("data:;base64,")[-1]
    data = base64.b64decode(base64_data)

    # Assume success for data URIs
    phony_response = requests.Response
    phony_response.status_code=200

    return (data, phony_response)


def fetch_remote_url(url: str or dict, params=None, headers=None) -> (bytes, object):
    data = b""

    if isinstance(url, dict):
        headers = url.get("headers", {})

    response = requests.get(url, headers=headers, params=params, stream=True)

    # with response as stream:
    #     for chunk in stream.iter_content(chunk_size=65536):
    #         if chunk:
    #             data += chunk

    return (data, response)


def fetch_url(url: str or dict, params={}, headers=None) -> (bytes, list):
    ''' Fetches and concatenates the payload htsget "urls" array with
        multiple urls where some of those urls contain base64-encoded
        data.

        Possible url inputs can be, i.e:
            1. http(s)://htsget.ga4gh-demo.org/(reads or variants)/id  ... str
            2. data:;base64,...                                            str
            3. Requests response dictionary containing dict(urls)          dict

        returns: Tuple with concatenated payload and a list of all responses from all URLs,
                 including embedded data:;<base64> urls.
    '''
    urls = []
    data = b""
    responses = []

    # Determine whether we have been given a "top-level htsget url" or something else
    if isinstance(url, str):
        # Data is the actual url so that next conditional can work on it as a dict
        url, response = fetch_remote_url(url, params, headers)
        responses.append(response)
    if isinstance(url, dict):
        urls = url.get("htsget", {}).get("urls", [])
        for entry in urls:
            url = entry.get("url")
            if url.startswith(("http://", "https://")):
                one_data, one_response = fetch_remote_url(url, params=params, headers=headers)
            elif url.startswith("data:;base64,"):
                one_data, one_response = fetch_inline_data(url)

            data += one_data
            responses.append(one_response)

    return data, responses

FORMAT_READS_URL = format_reads_url
FORMAT_VARIANTS_URL = format_variants_url

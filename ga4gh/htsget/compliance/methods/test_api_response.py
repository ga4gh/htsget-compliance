import json
import requests
from ga4gh.htsget.compliance.config import constants as c

def test_api_response(case, config):
    # print(case)
    # print(config)
    # print("***")

    url_template = case['url']
    url_dict = {
        "base_url": config["htsget_url"],
        "obj_id": case["obj_id"]
    }
    url = url_template.format(**url_dict)
    
    response = requests.get(url)
    response_json = response.json()
    
    


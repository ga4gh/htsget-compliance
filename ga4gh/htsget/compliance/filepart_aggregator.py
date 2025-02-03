import os
import shutil

from ga4gh.htsget.compliance.config import constants as c
from ga4gh.htsget.compliance.config import methods

class FilepartAggregator(object):
    
    def __init__(self, response):
        self.set_response(response)
        self.set_response_body()
        self.fileparts_dir = ".fileparts"
        if not os.path.exists(self.fileparts_dir):
            os.mkdir(self.fileparts_dir)
        self.set_output_filepath()

    def aggregate(self, params=None):
        response_body = self.get_response_body()
        i = 0
        for url_obj in response_body["htsget"]["urls"]:
            url = url_obj["url"]
            headers = url_obj["headers"] \
                      if "headers" in url_obj.keys() \
                      else None
            
            self.download_filepart(url, headers=headers, params=params, idx=i)
            i += 1
        
        self.aggregate_fileparts()

    def download_filepart(self, url, headers=None, params=None, idx=0):
        filepath = self.get_filepart_path(idx)
        with open(filepath, 'wb') as f:
            payload, _ = methods.fetch_url(url)
            f.write(payload)
    
    def aggregate_fileparts(self):
        with open(self.get_output_filepath(), 'wb') as wfd:
            for i in range(0, self.nfileparts):
                filepath = self.get_filepart_path(i)
                with open(filepath, 'rb') as fd:
                    shutil.copyfileobj(fd, wfd)

    def get_filepart_path(self, idx):
        return os.path.join(self.fileparts_dir, "{}.filepart".format(idx))
    
    def set_response(self, response):
        self.response = response
    
    def get_response(self):
        return self.response
    
    def set_response_body(self):
        self.response_body = self.get_response().json()
        self.nfileparts = len(self.response_body["htsget"]["urls"])
    
    def get_response_body(self):
        return self.response_body
    
    def set_output_filepath(self):
        extensions_dict = {
            c.FORMAT_BAM: c.EXTENSION_BAM,
            c.FORMAT_CRAM: c.EXTENSION_CRAM,
            c.FORMAT_VCF: c.EXTENSION_VCF,
            c.FORMAT_BCF: c.EXTENSION_BCF,
        }
        response_body = self.get_response_body()
        extension = extensions_dict[response_body["htsget"]["format"].upper()]
        fp = os.path.join(self.fileparts_dir, "file" + extension)
        self.output_filepath = fp
    
    def get_output_filepath(self):
        return os.path.abspath(self.output_filepath)

import os
import requests
from ga4gh.htsget.compliance.config import constants as c

class FileValidator(object):

    SUCCESS = 1
    FAILURE = -1

    def __init__(self, returned_fp, expected_fp):
        self.set_returned_fp(returned_fp)
        self.set_expected_fp(expected_fp)

    def identify_file(self, fp, source) -> str:
        '''
        source = from htsget or from (local) filesystem
        returns: file extension string
        '''
        ext = ""
        file_type = ""

        # TODO: This check shouldn't be here since htsfile is actually detecting files without extension?
        # need to read the .fileparts/* logic though and potentially move this function closer there...
        if not "." in fp:
            return "unknown"

        if "local_fs" in source:
            file_type = os.popen("htsfile " + fp)

        # Samtools' hstfile does not (yet) support (detailed?) htsget file identification ¯\_(ツ)_/¯
        #
        # % htsfile https://htsget.ga4gh-demo.org/reads/htsnexus_test_NA12878
        # https://htsget.ga4gh-demo.org/reads/htsnexus_test_NA12878:      htsget text
        elif "htsget" in source:
            file_type = requests.get(fp).json()["htsget"]["format"]

        # Determine the actual format and suitable extension
        if c.FORMAT_BAM in file_type:
            ext = c.EXTENSION_BAM
        elif c.FORMAT_CRAM in file_type:
            ext = c.EXTENSION_CRAM
        elif c.FORMAT_VCF in file_type:
            ext = c.EXTENSION_VCF
        elif c.FORMAT_BCF in file_type:
            ext = c.EXTENSION_BCF
        else:
            ext = ".unknown_file_format"
        
        return ext

    def validate(self):

        result = FileValidator.SUCCESS

        string_returned = self.load(self.get_returned_fp())
        string_expected = self.load(self.get_expected_fp())

        if string_returned != string_expected:
            result = FileValidator.FAILURE
        
        return result

    def load(self, fp) -> str:
        extension = ""
        samtools_string = ""

        if "http" in fp:
            extension = self.identify_file(fp, "htsget")
        else:
            extension = self.identify_file(fp, "local_fs")

        if not "unknown" in extension:
            samtools_string = self.load_binary(fp+extension)

        return samtools_string


    def load_binary(self, fp) -> str:
        s = []
        for line in os.popen("samtools view " + fp).readlines():
            ls = line.rstrip().split("\t")
            s.append("\t".join(ls[:11]))
        return "\n".join(s) + "\n"

    def set_returned_fp(self, returned_fp):
        self.returned_fp = returned_fp
    
    def get_returned_fp(self):
        return self.returned_fp
    
    def set_expected_fp(self, expected_fp):
        self.expected_fp = expected_fp
    
    def get_expected_fp(self):
        return self.expected_fp
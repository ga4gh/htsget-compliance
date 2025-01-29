import os
import requests
from ga4gh.htsget.compliance.config import constants as c
from ga4gh.htsget.compliance.config import methods
import tempfile

class FileValidator(object):

    SUCCESS = 1
    FAILURE = -1

    def __init__(self, returned_fp, expected_fp):
        self.set_returned_fp(returned_fp)
        self.set_expected_fp(expected_fp)

    def is_encrypted_with(self, fp) -> str:
        ''' Identifies encryption scheme
        '''
        encryption_scheme = None
        encryption_scheme = os.popen("htsfile " + fp)
        if "crypt4gh data" in encryption_scheme:
            encryption_scheme = c.ENCRYPTION_SCHEME_CRYPT4GH
        # Must be last statement if no scheme is found above
        else:
            encryption_scheme = None

        return encryption_scheme

    def identify_file(self, fp, source) -> (str, str):
        '''
        source = from htsget or from (local) filesystem
        returns: tuple encoding file extension and encryption scheme (if any)
        '''
        ext = None
        file_type = None
        encryption_scheme = None

        # TODO: This check shouldn't be here since htsfile is actually detecting files without extension?
        # need to read the .fileparts/* logic though and potentially move this function closer there...
        if not "." in fp:
            return "unknown"
        # FIXME: Also breaks with filenames such as spec-v4.3, i.e:
        # htsfile: can't open "/Users/rvalls/dev/umccr/htsget-compliance/ga4gh/htsget/data/variants/spec-v4.3": No such file or directory
        # elif basename(fp) == "spec-v4.3":
        #     return "unknown"

        if "local_fs" in source:
            encryption_scheme = self.is_encrypted_with(fp)

        # Samtools' hstfile does not (yet) support (detailed?) htsget file identification ¯\_(ツ)_/¯
        #
        # % htsfile https://htsget.ga4gh-demo.org/reads/htsnexus_test_NA12878
        # https://htsget.ga4gh-demo.org/reads/htsnexus_test_NA12878:      htsget text
        elif "htsget" in source:
            file_payload, responses = methods.get_urls_concatenate_output(fp).json()
            file_type = responses[0]["htsget"]["format"] # First response code is from htsget endpoint itself

            with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                temp_file.write(file_payload.encode())
                temp_file.flush()
                encryption_scheme = self.is_encrypted_with(temp_file.name)


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
        
        return (ext, encryption_scheme)

    def validate(self):

        result = FileValidator.SUCCESS

        string_returned = self.load(self.get_returned_fp())
        string_expected = self.load(self.get_expected_fp())

        if string_returned != string_expected:
            result = FileValidator.FAILURE
        
        return result

    def load(self, fp) -> str:
        extension = None
        encrypted = None
        samtools_string = None

        if "http" in fp:
            (extension, encrypted) = self.identify_file(fp, "htsget")
        else:
            (extension, encrypted) = self.identify_file(fp, "local_fs")

        if not "unknown" in extension:
            samtools_string = self.load_binary(fp+extension)
        elif encrypted is not None:
            if encryption_scheme == c.ENCRYPTION_SCHEME_CRYPT4GH:
                cleartext_string = self.decrypt_c4gh_binary(fp, private_key)

        return samtools_string

    def decrypt_c4gh_binary(self, fp) -> str:
        pass

    def load_binary(self, fp) -> str:
        s = []
        viewer_ouput = ""

        if "bcf" in fp:
            viewer_ouput = os.popen("bcftools view " + fp).readlines()
        else:
            viewer_output = os.popen("samtools view " + fp).readlines()

        for line in viewer_output:
            ls = line.rstrip().split("\t")
            s.append("\t".join(ls[:11])) # TODO: Probably a hashed output would be more reliable, efficient and no so dependant on samtools?
        return "\n".join(s) + "\n"

    def set_returned_fp(self, returned_fp):
        self.returned_fp = returned_fp
    
    def get_returned_fp(self):
        return self.returned_fp
    
    def set_expected_fp(self, expected_fp):
        self.expected_fp = expected_fp
    
    def get_expected_fp(self):
        return self.expected_fp
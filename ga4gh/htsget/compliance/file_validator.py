import os
import tempfile

from ga4gh.htsget.compliance.config import constants as c
from ga4gh.htsget.compliance.config import methods

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

        # FIXME:
        # (...)
        # htsfile: can't open "/Users/rvalls/dev/umccr/htsget-compliance/ga4gh/htsget/data/reads/htsnexus_test_NA12878": No such file or directory
        # htsfile: can't open "/Users/rvalls/dev/umccr/htsget-compliance/ga4gh/htsget/data/reads/htsnexus_test_NA12878": No such file or directory
        # htsfile: can't open "/Users/rvalls/dev/umccr/htsget-compliance/ga4gh/htsget/data/reads/htsnexus_test_NA12878": No such file or directory
        # htsfile: can't open "/Users/rvalls/dev/umccr/htsget-compliance/ga4gh/htsget/data/variants/spec-v4.3": No such file or directory
        # htsfile: can't open "/Users/rvalls/dev/umccr/htsget-compliance/ga4gh/htsget/data/variants/spec-v4.3": No such file or directory
        # htsfile: can't open "/Users/rvalls/dev/umccr/htsget-compliance/ga4gh/htsget/data/variants/spec-v4.3": No such file or directory
        # (...)

        if "local_fs" in source:
            encryption_scheme = self.is_encrypted_with(fp)
            file_type = os.popen("htsfile " + fp)

        # Samtools' hstfile does not (yet) support (detailed?) htsget file identification ¯\_(ツ)_/¯
        #
        # % htsfile https://htsget.ga4gh-demo.org/reads/htsnexus_test_NA12878
        # https://htsget.ga4gh-demo.org/reads/htsnexus_test_NA12878:      htsget text
        elif "htsget" in source:
            file_payload, responses = methods.fetch_url(fp).json()
            file_type = responses[0]["htsget"]["format"] # First response code is from htsget endpoint itself

            # htsfile needs a file
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

        # Append encryption file extension to file type if encrypted
        if encryption_scheme is not None:
            if encryption_scheme == c.ENCRYPTION_SCHEME_CRYPT4GH:
                ext = ext + c.EXTENSION_C4GH
        
        return (ext, encryption_scheme)

    def validate(self):

        result = FileValidator.SUCCESS

        string_returned = self.load(self.get_returned_fp())
        string_expected = self.load(self.get_expected_fp())

        if string_returned != string_expected:
            result = FileValidator.FAILURE
        if string_expected is None:
            result = FileValidator.FAILURE
        if string_returned is None:
            result = FileValidator.FAILURE
        
        return result

    def load(self, fp) -> str:
        extension = None
        encrypted = None
        payload = None
        private_key = c.PRIVATE_KEY_CRYPT4GH

        # if fp.startswith(("http://", "https://")):
        #     (extension, encrypted) = self.identify_file(fp, "htsget")
        # else:
        (extension, encrypted) = self.identify_file(fp, "local_fs")

        if "unknown" not in extension:
            payload = self.load_binary(fp+extension)
        if encrypted is not None:
            if encrypted == c.ENCRYPTION_SCHEME_CRYPT4GH:
                payload = self.decrypt_c4gh_binary(fp + c.EXTENSION_C4GH, private_key)

        return payload

    def decrypt_c4gh_binary(self, fp, private_key) -> str:
        return os.popen("crypt4gh decrypt --sk " + private_key + " < " + fp).readlines()

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
import os

class FileValidator(object):

    SUCCESS = 1
    FAILURE = -1

    def __init__(self, returned_fp, expected_fp):
        self.set_returned_fp(returned_fp)
        self.set_expected_fp(expected_fp)
    
    def validate(self):

        result = FileValidator.SUCCESS

        string_returned = self.load(self.get_returned_fp())
        string_expected = self.load(self.get_expected_fp())

        if string_returned != string_expected:
            result = FileValidator.FAILURE
        
        return result

    def load(self, fp):
        file_type = os.popen("htsfile " + fp)
        ext = ""
        s = ""

        if 'BAM' in file_type:
            ext = ".bam"
        elif 'CRAM' in file_type:
            ext = ".cram"
        elif 'VCF' in file_type:
            ext = ".vcf.gz"
        elif 'BCF' in file_type:
            ext = "bcf"
        else:
            s = self.load_binary(fp+ext)

        return s

    def load_binary(self, fp):
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
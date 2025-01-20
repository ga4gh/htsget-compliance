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

        s = ""
        if fp.endswith(".bam"):
            s = self.load_bam(fp)
        
        return s

    def load_sam(self, fp):
        s = []
        header = True
        with open(fp, "r") as f:
            for line in f.readlines():
                
                if header:
                    if not line.startswith("@"):
                        header = False
                
                if not header:
                    ls = line.rstrip().split("\t")
                    s.append("\t".join(ls[:11]))
        return "\n".join(s) + "\n"

    def load_bam(self, fp):
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

from ga4gh.testbed import constants as c

class ReportCase(object):

    def __init__(self):
        self.name = None
        self.status = None
        self.debug = []
        self.info = []
        self.warn = []
        self.error = None
    
    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def set_status_success(self):
        self.status = c.RESULT_SUCCESS

    def set_status_warning(self):
        self.status = c.RESULT_WARNING

    def set_status_failure(self):
        self.status = c.RESULT_FAILURE

    def set_status_skipped(self):
        self.status = c.RESULT_SKIPPED
    
    def get_status(self):
        return self.status
    
    def add_debug_msg(self, message):
        self.debug.append(message)
    
    def get_debug(self):
        return self.debug
    
    def add_info_msg(self, message):
        self.info.append(message)

    def get_info(self):
        return self.info
    
    def add_warn_msg(self, message):
        self.warn.append(message)
    
    def get_warn(self):
        return self.warn
    
    def set_error(self, message):
        self.error = message
    
    def get_error(self):
        return self.error

    def as_json(self):
        return {
            "name": self.name,
            "status": self.get_status(),
            "debug": self.get_debug(),
            "info": self.get_info(),
            "warn": self.get_warn(),
            "error": self.get_error()
        }
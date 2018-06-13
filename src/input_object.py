'''
Created on May 7, 2018

@author: adameb
'''

class InputObject:
    def __init__(self, gvkey, cik, obfirm, wrdsfname, fdate, conf_call_filename):
        self.gvkey = gvkey
        self.cik = cik
        self.conf_call_filename = conf_call_filename
        self.obfirm = obfirm
        self.wrdsfname = wrdsfname
        self.fdate = fdate
        
    def __str__(self):
        return "InputObject(cik: {}, conf_call_filename: {}, fdate: {}, gvkey: {}, obfirm: {}, wrdsfname: {})".format(
            self.cik, self.conf_call_filename, self.fdate, self.gvkey, self.obfirm, self.wrdsfname)
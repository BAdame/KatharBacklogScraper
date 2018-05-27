'''
Created on May 8, 2018

@author: adameb
'''

class OutputObject:
    def __init__(self,
        # '0/1 variable: 0 if "backlog" is NOT mentioned; 1 if "backlog" is mentioned
        blog_mention = 0,

        # 0/1 variable: 1 if ANY mention of "backlog" is within the same sentence of 
        # "%", "$", "million", "billion", "percent", or "dollars"; 0 otherwise
        blog_quant = 0,

        # shortest distance (in characters) between any mention of backlog and any of the 
        # existing quantitative phrases/characters - max of 300        
        blog_quant_dist = -1,
        
        # shortest distance (in characters) between any mention of backlog
        blog_sh_dist = 0,
        
        # sum of the number of characters in the same sentence as any mention of backlog. 
        # Example: if the only mentions of backlog were: 
        # "Backlog sucked. Don't ask about our backlog." this would take the value of 44.
        blog_sent = 0, 
        
        cik = '', 
        
        conf_call_filename = '',
        
        fdate = '',
        
        gvkey = '',
        
        # number of backlog mentions
        nblog_mention = 0,
        
        # 0/1 variable: 1 if ANY mention of "backlog" is within 100 characters of 
        # any of the following terms: 
        # "reduction", "decreas", "decline", "below", "lower", "down", "weak"
        neg_blog = 0,
        
        neg_blog_dist = 0,
        
        # Number of times a negative word was in the same sentence as backlog
        num_negblog = 0,

        # Number of times a positive word was in the same sentence as backlog
        num_posblog = 0,
        
        obfirm = 0,
        
        # 0/1 variable: 1 if ANY mention of "backlog" is within 100 characters of
        # any of the following terms: 
        # "grow", "increas", "strong", "grew", "high", "improve", "record" (but NOT "recorded")
        pos_blog = 0,
        
        pos_blog_dist = 0,
        
        wrdsfname = ''):
        self.blog_mention = blog_mention
        self.blog_quant = blog_quant
        self.blog_quant_dist = blog_quant_dist
        self.blog_sent = blog_sent
        self.blog_sh_dist = blog_sh_dist
        self.cik = cik
        self.conf_call_filename = conf_call_filename
        self.fdate = fdate
        self.gvkey = gvkey
        self.nblog_mention = nblog_mention
        self.neg_blog = neg_blog
        self.neg_blog_dist = neg_blog_dist
        self.num_negblog = num_negblog
        self.num_posblog = num_posblog
        self.obfirm = obfirm
        self.pos_blog = pos_blog
        self.pos_blog_dist = pos_blog_dist
        self.wrdsfname = wrdsfname
        
    def getCsv(self):
        '''
        Gets the object as a CSV row.
        Columns aligned with the getCsvHeaders() method.
        TODO: Use reflection to guarantee the ordering is always the same.
        '''
        return "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
            self.blog_mention, 
            self.blog_quant,
            self.blog_quant_dist,
            self.blog_sent, 
            self.blog_sh_dist, 
            self.cik, 
            self.conf_call_filename, 
            self.fdate, 
            self.gvkey, 
            self.nblog_mention,
            self.neg_blog, 
            self.neg_blog_dist, 
            self.num_negblog,
            self.num_posblog, 
            self.obfirm, 
            self.pos_blog, 
            self.pos_blog_dist, 
            self.wrdsfname)
    
    @staticmethod
    def getCsvHeaders():
        '''
        Get the headers for a CSV.
        Columns aligned with the getCsv(self) method.
        '''
        return "blog_mention,blog_quant,blog_quant_dist,blog_sent,blog_sh_dist,cik,conf_call_filename,fdate,gvkey,nblog_mention,neg_blog,neg_blog_dist,num_negblog,num_posblog,obfirm,pos_blog,pos_blog_dist,wrdsfname\n"
        
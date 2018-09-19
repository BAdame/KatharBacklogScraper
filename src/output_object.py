"""
Created on May 8, 2018

@author: adameb
"""


class OutputObject:
    def __init__(self,
                 # Number of times 'backlog amortization' is mentioned
                 amor_blog_mention = 0,

                 # '0/1 variable: 0 if "backlog" is NOT mentioned; 1 if "backlog" is mentioned
                 blog_mention=0,

                 # 0/1 variable: 1 if ANY mention of "backlog" is within the same sentence of
                 # "%", "$", "million", "billion", "percent", or "dollars"; 0 otherwise
                 blog_quant=0,

                 # shortest distance (in characters) between any mention of backlog and any of the
                 # existing quantitative phrases/characters - max of 300
                 blog_quant_dist=-1,

                 # Same as blog_quant, but doesn't detect newlines as sentence markers
                 blog_quant_no_newlines = 0,

                 # 0/1 variable: 1 if there's a 3+ digit number soon after a backlog mention.
                 # This is to detect quant mentions in tables, which aren't detected as sentences.
                 blog_quant_table=0,

                 # shortest distance (in characters) between any mention of backlog
                 blog_sh_dist=0,

                 # sum of the number of characters in the same sentence as any mention of backlog.
                 # Example: if the only mentions of backlog were:
                 # "Backlog sucked. Don't ask about our backlog." this would take the value of 44.
                 blog_sent=0,

                 # The text around 'backlog' mentions
                 blog_surrounding_text='',

                 bs_ind=0,

                 cik='',

                 conf_call_filename='',

                 doc_length = -1,

                 fdate='',

                 first_mention_loc = -1,

                 fls_sent = 0,

                 fls_sent_earn = 0,

                 fls_sent_quant = 0,

                 gvkey='',

                 mentioner_names = '',

                 # number of backlog mentions
                 nblog_mention=0,

                 # 0/1 variable: 1 if ANY mention of "backlog" is within 100 characters of
                 # any of the following terms:
                 # "reduction", "decreas", "decline", "below", "lower", "down", "weak"
                 neg_blog=0,

                 neg_blog_dist=0,

                 # Number of times a negative word was in the same sentence as backlog
                 num_negblog=0,

                 # Number of times a positive word was in the same sentence as backlog
                 num_posblog=0,

                 n_sent=0,

                 obfirm=0,

                 # 0/1 variable: 1 if ANY mention of "backlog" is within 100 characters of
                 # any of the following terms:
                 # "grow", "increas", "strong", "grew", "high", "improve", "record" (but NOT "recorded")
                 pos_blog=0,

                 pos_blog_dist=0,

                 wrdsfname=''):
        self.amor_blog_mention = amor_blog_mention
        self.blog_mention = blog_mention
        self.blog_quant = blog_quant
        self.blog_quant_dist = blog_quant_dist
        self.blog_quant_no_newlines = blog_quant_no_newlines
        self.blog_quant_table = blog_quant_table
        self.blog_sent = blog_sent
        self.blog_sh_dist = blog_sh_dist
        self.blog_surrounding_text = blog_surrounding_text
        self.bs_ind = bs_ind
        self.cik = cik
        self.conf_call_filename = conf_call_filename
        self.doc_length = doc_length
        self.fdate = fdate
        self.first_mention_loc = first_mention_loc
        self.fls_sent = fls_sent
        self.fls_sent_earn = fls_sent_earn
        self.fls_sent_quant = fls_sent_quant
        self.gvkey = gvkey
        self.mentioner_names = mentioner_names
        self.nblog_mention = nblog_mention
        self.neg_blog = neg_blog
        self.neg_blog_dist = neg_blog_dist
        self.num_negblog = num_negblog
        self.num_posblog = num_posblog
        self.n_sent = n_sent
        self.obfirm = obfirm
        self.pos_blog = pos_blog
        self.pos_blog_dist = pos_blog_dist
        self.wrdsfname = wrdsfname

    def get_csv(self):
        """
        Gets the object as a CSV row.
        Columns aligned with the getCsvHeaders() method.
        TODO: Use another pattern to guarantee the ordering is always the same.
        """
        return "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
            self.amor_blog_mention,
            self.blog_mention,
            self.blog_quant,
            self.blog_quant_dist,
            self.blog_quant_no_newlines,
            self.blog_quant_table,
            self.blog_sent,
            self.blog_sh_dist,
            self.blog_surrounding_text,
            self.bs_ind,
            self.cik,
            self.conf_call_filename,
            self.doc_length,
            self.fdate,
            self.first_mention_loc,
            self.fls_sent,
            self.fls_sent_earn,
            self.fls_sent_quant,
            self.gvkey,
            self.mentioner_names,
            self.nblog_mention,
            self.neg_blog,
            self.neg_blog_dist,
            self.num_negblog,
            self.num_posblog,
            self.n_sent,
            self.obfirm,
            self.pos_blog,
            self.pos_blog_dist,
            self.wrdsfname)

    @staticmethod
    def get_csv_headers():
        '''
        Get the headers for a CSV.
        Columns aligned with the getCsv(self) method.
        '''
        return "amor_blog_mention," \
               "blog_mention," \
               "blog_quant," \
               "blog_quant_dist," \
               "blog_quant_no_newlines," \
               "blog_quant_table," \
               "blog_sent," \
               "blog_sh_dist," \
               "blog_surrounding_text," \
               "bs_ind," \
               "cik," \
               "conf_call_filename," \
               "doc_length," \
               "fdate," \
               "first_mention_loc," \
               "fls_sent," \
               "fls_sent_earn," \
               "fls_sent_quant," \
               "gvkey," \
               "mentioner_names," \
               "nblog_mention," \
               "neg_blog," \
               "neg_blog_dist," \
               "num_negblog," \
               "num_posblog," \
               "n_sent," \
               "obfirm," \
               "pos_blog," \
               "pos_blog_dist," \
               "wrdsfname\n"

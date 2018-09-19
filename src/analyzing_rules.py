import re
from output_object import OutputObject

# Punctuation defining end of sentences
end_of_sentence_markers = ["? ", "! ", ". ", ".\t", "\n", "\r", '."', ".'", u"\u2022",  # Bullet point
                           ]
end_of_sentence_markers_no_newlines = ["? ", "! ", ". ", '."', ".'", ".\t", u"\u2022",  # Bullet point
                                       ]
bsPhrases = ["balance sheet", "statement of financial position"]
earningsPhrases = ["earnings", "eps", "income", "loss", "profit"]
quantPhrasesToMatch = ["%", "$", "million", "billion", "percent", "dollars",
                       " units", "home", "house", 'railcar', "theater"]
quantPhrasesRegexes = ["%", "\\$", "million", "billion", "percent", "dollars",
                       " units", "home", "house", 'railcar', "theater"]
negPhrasesToMatch = ["reduction", "decreas", "decline", "below", "lower", "down", "weak", "reduced", "negatively"]
posPhrasesToMatch = ["grow", "increas", "strong", "grew", "high", "improve", "record"]
flsPhrasesToMatch = ["also aim", "and forecast", "are seeking", "company believes", "also aims", "and forecasts", "are sought", "company commits", "also anticipate", "and foresee", "are targeted", "company estimates", "also anticipates", "and foresees", "are targeting", "company expects", "also assume", "and hope", "are willing", "company forecasts", "also assumes", "and hopes", "assume", "company foresees", "also believe", "and intend", "assumes", "company hopes", "also believes", "and intends", "believe", "company intends", "also commit", "and plan", "believes", "company plans", "also commits", "and plans", "but aim", "company projects", "also estimate", "and project", "but aims", "company seeks", "also estimates", "and projects", "but anticipate", "company targets", "also expect", "and seek", "but anticipates", "corporation aims", "also expects", "and seeks", "but assume", "corporation anticipates", "also forecast", "and target", "but assumes", "corporation assumes", "also forecasts", "and targets", "but believe", "corporation believes", "also foresee", "and will", "but believes", "corporation commits", "also foresees", "anticipate", "but commit", "corporation estimates", "also hope", "anticipates", "but commits", "corporation expects", "also hopes", "are aimed", "but estimate", "corporation forecasts", "also intend", "are aiming", "but estimates", "corporation foresees", "also intends", "are anticipated", "but expect", "corporation hopes", "also plan", "are anticipating", "but expects", "corporation intends", "also plans", "are assumed", "but forecast", "corporation plans", "also project", "are assuming", "but forecasts", "corporation projects", "also projects", "are believed", "but foresee", "corporation seeks", "also seek", "are believing", "but foresees", "corporation targets", "also seeks", "are committed", "but hope", "currently aim", "also target", "are committing", "but hopes", "currently aimed", "also targets", "are estimated", "but intend", "currently aiming", "also will", "are estimating", "but intends", "currently aims", "and aim", "are expected", "but plan", "currently anticipate", "and aims", "are expecting", "but plans", "currently anticipated", "and anticipate", "are forecasted", "but project", "currently anticipates", "and anticipates", "are forecasting", "but projects", "currently anticipating", "and assume", "are foreseeing", "but seek", "currently assume", "and assumes", "are foreseen", "but seeks", "currently assumed", "and believe", "are hoped", "but target", "currently assumes", "and believes", "are hoping", "but targets", "currently assuming", "and commit", "are intended", "but will", "currently believe", "and commits", "are intending", "commit", "currently believed", "and estimate", "are planed", "commits", "currently believes", "and estimates", "are planning", "company aims", "currently believing", "and expect", "are projected", "company anticipates", "currently commit", "and expects", "are projecting", "company assumes", "currently commits", "currently committed", "do not anticipate", "firm projects", "management forecasts", "currently committing", "do not assume", "firm seeks", "management foresees", "currently estimate", "do not believe", "firm targets", "management hopes", "currently estimated", "do not commit", "foresee", "management intends", "currently estimates", "do not estimate", "foresees", "management plans", "currently estimating", "do not expect", "intend", "management projects", "currently expect", "do not forecast", "intends", "management seeks", "currently expected", "do not foresee", "is aimed", "management targets", "currently expecting", "do not hope", "is aiming", "normally aim", "currently expects", "do not intend", "is anticipated", "normally aims", "currently forecast", "do not plan", "is anticipating", "normally anticipate", "currently forecasted", "do not project", "is assumed", "normally anticipates", "currently forecasting", "do not seek", "is assuming", "normally assume", "currently forecasts", "do not target", "is believed", "normally assumes", "currently foresee", "do not will", "is believing", "normally believe", "currently foreseeing", "does not aim", "is committed", "normally believes", "currently foreseen", "does not anticipate", "is committing", "normally commit", "currently foresees", "does not assume", "is estimated", "normally commits", "currently hope", "does not believe", "is estimating", "normally estimate", "currently hoped", "does not commit", "is expected", "normally estimates", "currently hopes", "does not estimate", "is expecting", "normally expect", "currently hoping", "does not expect", "is forecasted", "normally expects", "currently intend", "does not forecast", "is forecasting", "normally forecast", "currently intended", "does not foresee", "is foreseeing", "normally forecasts", "currently intending", "does not hope", "is foreseen", "normally foresee", "currently intends", "does not intend", "is hoped", "normally foresees", "currently plan", "does not plan", "is hoping", "normally hope", "currently planed", "does not project", "is intended", "normally hopes", "currently planning", "does not seek", "is intending", "normally intend", "currently plans", "does not target", "is planed", "normally intends", "currently project", "does not will", "is planning", "normally plan", "currently projected", "expect", "is projected", "normally plans", "currently projecting", "expects", "is projecting", "normally project", "currently projects", "firm aims", "is seeking", "normally projects", "currently seek", "firm anticipates", "is sought", "normally seek", "currently seeking", "firm assumes", "is targeted", "normally seeks", "currently seeks", "firm believes", "is targeting", "normally target", "currently sought", "firm commits", "is willing", "normally targets", "currently target", "firm estimates", "management aims", "normally will", "currently targeted", "firm expects", "management anticipates", "not aimed", "currently targeting", "firm forecasts", "management assumes", "not aiming", "currently targets", "firm foresees", "management believes", "not anticipated", "currently will", "firm hopes", "management commits", "not anticipating", "currently willing", "firm intends", "management estimates", "not assumed", "do not aim", "firm plans", "management expects", "not assuming", "not believed", "now estimate", "still aimed", "still planning", "not believing", "now estimated", "still aiming", "still plans", "not committed", "now estimates", "still aims", "still project", "not committing", "now estimating", "still anticipate", "still projected", "not estimated", "now expect", "still anticipated", "still projecting", "not estimating", "now expected", "still anticipates", "still projects", "not expected", "now expecting", "still anticipating", "still seek", "not expecting", "now expects", "still assume", "still seeking", "not forecasted", "now forecast", "still assumed", "still seeks", "not forecasting", "now forecasted", "still assumes", "still sought", "not foreseeing", "now forecasting", "still assuming", "still target", "not foreseen", "now forecasts", "still believe", "still targeted", "not hoped", "now foresee", "still believed", "still targeting", "not hoping", "now foreseeing", "still believes", "still targets", "not intended", "now foreseen", "still believing", "still will", "not intending", "now foresees", "still commit", "still willing", "not planed", "now hope", "still commits", "we aim", "not planning", "now hoped", "still committed", "we anticipate", "not projected", "now hopes", "still committing", "we assume", "not projecting", "now hoping", "still estimate", "we believe", "not seeking", "now intend", "still estimated", "we commit", "not sought", "now intended", "still estimates", "we estimate", "not targeted", "now intending", "still estimating", "we expect", "not targeting", "now intends", "still expect", "we forecast", "not willing", "now plan", "still expected", "we foresee", "now aim", "now planed", "still expecting", "we hope", "now aimed", "now planning", "still expects", "we intend", "now aiming", "now plans", "still forecast", "we plan", "now aims", "now project", "still forecasted", "we project", "now anticipate", "now projected", "still forecasting", "we seek", "now anticipated", "now projecting", "still forecasts", "we target", "now anticipates", "now projects", "still foresee", "we will", "now anticipating", "now seek", "still foreseeing", "will", "now assume", "now seeking", "still foreseen", "now assumed", "now seeks", "still foresees", "now assumes", "now sought", "still hope", "now assuming", "now target", "still hoped", "now believe", "now targeted", "still hopes", "now believed", "now targeting", "still hoping", "now believes", "now targets", "still intend", "now believing", "now will", "still intended", "now commit", "now willing", "still intending", "now commits", "seek", "still intends", "now committed", "seeks", "still plan", "now committing", "still aim", "still planed"]

def get_output_object(input_object, raw_text, is_transcript = False):
    # Find all the locations of 'backlog' in the text
    backlog_mention_locations = [it.start() for it in re.finditer('backlog', raw_text)]

    return OutputObject(
                    amor_blog_mention=get_amor_blog_mention(raw_text, backlog_mention_locations),
                    blog_mention=get_blog_mention(raw_text, backlog_mention_locations),
                    blog_quant=get_blog_quant(raw_text, backlog_mention_locations),
                    blog_quant_dist=get_blog_quant_dist(raw_text, backlog_mention_locations),
                    blog_quant_no_newlines=get_blog_quant_no_newlines(raw_text, backlog_mention_locations),
                    blog_quant_table=get_blog_quant_table(raw_text, backlog_mention_locations),
                    blog_sent=get_blog_sent(raw_text, backlog_mention_locations),
                    blog_sh_dist=get_blog_sh_dist(raw_text, backlog_mention_locations),
                    blog_surrounding_text=get_blog_surrounding_text(raw_text, backlog_mention_locations),
                    bs_ind=get_bs_ind(raw_text),
                    cik=input_object.cik,
                    conf_call_filename=input_object.conf_call_filename,
                    doc_length = len(raw_text),
                    fdate=input_object.fdate,
                    first_mention_loc = -1 if len(backlog_mention_locations) is 0 else backlog_mention_locations[0],
                    fls_sent=get_fls_sent(raw_text),
                    fls_sent_earn=get_fls_earn(raw_text),
                    fls_sent_quant=get_fls_sent_quant(raw_text),
                    gvkey=input_object.gvkey,
                    mentioner_names = get_mentioner_names(raw_text, backlog_mention_locations) if is_transcript else ' ',
                    nblog_mention=get_n_blog_mention(raw_text, backlog_mention_locations),
                    neg_blog=get_neg_blog(raw_text, backlog_mention_locations),
                    neg_blog_dist=get_closest_distance_to_phrases(raw_text, backlog_mention_locations, 200,
                                                                  negPhrasesToMatch),
                    num_negblog=get_num_neg_blog(raw_text, backlog_mention_locations),
                    num_posblog=get_num_pos_blog(raw_text, backlog_mention_locations),
                    n_sent=get_n_sent(raw_text),
                    obfirm=input_object.obfirm,
                    pos_blog=get_pos_blog(raw_text, backlog_mention_locations),
                    pos_blog_dist=get_closest_distance_to_phrases(raw_text, backlog_mention_locations, 200,
                                                                  posPhrasesToMatch),
                    wrdsfname=input_object.wrdsfname
                )

def get_bs_ind(raw_text):
    for phrase in bsPhrases:
        if phrase in raw_text:
            return 1
    return 0

# Count of 'amortized backlog' or 'backlog amortization'
def get_blog_mention(text, matching_indices):
    return 1 if (len(matching_indices) > 0) else 0

# '0/1 variable: 0 if "backlog" is NOT mentioned; 1 if "backlog" is mentioned
def get_blog_quant(text, matching_indices):
    for index in matching_indices:
        words_around_backlog = get_sentence(text, index)
        for phrase in quantPhrasesToMatch:
            if phrase in words_around_backlog:
                return 1
    return 0

# number of sentences that contain an fls phrase
def get_fls_sent(text):
    sentences = set()
    for phrase in flsPhrasesToMatch:
        mentions = [it.start() for it in re.finditer(phrase, text)]
        for i in mentions:
            sentences.add(get_sentence(text, i, end_of_sentence_markers_no_newlines))

    return len(sentences)

# returns the number of sentences where forward looking words are mentioned in the same sentence as an earnings word
def get_fls_earn(text):
    return get_fls_sent_intersect(text, earningsPhrases)

# returns the number of sentences where forward looking words are mentioned in the same sentence as a quant word
def get_fls_sent_quant(text):
    return get_fls_sent_intersect(text, quantPhrasesRegexes)

def get_fls_sent_intersect(text, phrases):
    all_mentions = []
    for phrase in phrases:
        phrase_mentions = [it.start() for it in re.finditer(phrase, text)]
        all_mentions.extend(phrase_mentions)

    all_sentences = set()
    for i in all_mentions:
        sentence = get_sentence(text, i)
        all_sentences.add(sentence)

    phrase_sentences = set()
    for sentence in all_sentences:
        for flsPhrase in flsPhrasesToMatch:
            if flsPhrase in sentence:
                phrase_sentences.add(sentence)

    return len(phrase_sentences)

# Number of sentences in the text
def get_n_sent(text):
    sentences = 0
    for marker in end_of_sentence_markers_no_newlines:
        sentences += text.count(marker)

    return sentences

# 0/1 variable: 1 if ANY mention of "backlog" is within the same sentence of
# "%", "$", "million", "billion", "percent", or "dollars"; 0 otherwise
def get_blog_quant_no_newlines(text, matching_indices):
    for index in matching_indices:
        words_around_backlog = get_sentence(text, index, end_of_sentence_markers_no_newlines)
        for phrase in quantPhrasesToMatch:
            if phrase in words_around_backlog:
                return 1
    return 0


# 0/1 variable: 1 if ANY mention of "backlog" is within the same sentence of
# "%", "$", "million", "billion", "percent", or "dollars"; 0 otherwise
def get_blog_sent(text, matching_indices):
    sentences = set()
    for index in matching_indices:
        sentences.add(get_sentence(text, index))

    return len(sentences)


# Number of sentences backlog was mentioned in
# Example: if the only mentions of backlog were:
# "Backlog sucked. Don't ask about our backlog." this would take the value of 2.
def get_blog_quant_dist(text, matching_indices, chars_to_search=300):
    return get_closest_distance_to_phrases(text, matching_indices, chars_to_search, quantPhrasesToMatch)


# shortest distance (in characters) between any mention of backlog and any of the
# existing quantitative phrases/characters - max of 300
def get_blog_quant_table(text, matching_indices, chars_to_search=50):
    for index in matching_indices:
        text_after_backlog = text[index: index + chars_to_search]
        # Match at least 3 digits in a row, excluding commas
        number_matches = re.findall('[0-9]{1,3}(,([0-9]{3}))+|([^0-9]\d{3}[^0-9])', text_after_backlog)
        if len(number_matches) > 0 and len(number_matches[0]) > 0:
            return 1
    return 0


def get_blog_sh_dist(text, matching_indices, chars_to_search=5000):
    phrases_to_match = ["non-gaap", "non gaap", "safe harbor", "private securities litigation reform",
                        "forward-looking", "forward looking"]
    return get_closest_distance_to_phrases(text, matching_indices, chars_to_search, phrases_to_match)


# shortest distance (in characters) between any mention of backlog
def get_blog_surrounding_text(text, matching_indices, chars_to_search=150):
    text_separator = '   -----------   '
    text_to_return = ''
    for index in matching_indices:
        surrounding_text = text[max(0, index - chars_to_search): min(len(text), index + chars_to_search)]
        text_to_return += surrounding_text + text_separator
    return re.sub('["\n\r\t,]', ' ', text_to_return)


# shortest distance (in characters) between any mention of backlog
def get_n_blog_mention(text, matching_indices):
    return len(matching_indices)


def get_amor_blog_mention(text, matching_indices):
    phrases_to_match = ['backlog amortization', 'amortization of backlog']
    num_mentions = 0
    for phrase in phrases_to_match:
        matches = re.findall(phrase, text)
        num_mentions += len(matches)
    return num_mentions
# number of backlog mentions


def get_mentioner_names(text, matching_indices):
    speaker_separator = '------'
    lines = text.split('\n')
    if len(lines) < 3:
        return ''

    current = lines[2]
    prev_1 = lines[1]
    prev_2 = lines[0]
    names = set()
    # Start on the 3rd line
    for line in lines[3 : ]:
        # Move pointers
        prev_2 = prev_1
        prev_1 = current
        current = line

        if 'backlog' in line and speaker_separator in prev_1:
            name = prev_2.split('[')[0].strip().replace(',', '')
            names.add(name)
    return ' ; '.join(names)

def get_neg_blog(text, matching_indices):
    for index in matching_indices:
        words_around_backlog = get_sentence(text, index)
        for phrase in negPhrasesToMatch:
            if phrase in words_around_backlog:
                return 1
    return 0
# 0/1 variable: 1 if ANY mention of "backlog" is in the same sentence as of
# any of the following terms:
# "reduction", "decreas", "decline", "below", "lower", "down", "weak"


def get_num_neg_blog(text, matching_indices):
    return get_num_phrases_in_sentences(text, matching_indices, negPhrasesToMatch)
# Number of times a negative word was in the same sentence as backlog


def get_num_pos_blog(text, matching_indices):
    return get_num_phrases_in_sentences(text, matching_indices, posPhrasesToMatch)
# Number of times a positive word was in the same sentence as backlog


def get_pos_blog(text, matching_indices):
    phrases_to_omit = ["recorded"]
    for index in matching_indices:
        words_around_backlog = get_sentence(text, index)
        for posPhrase in posPhrasesToMatch:
            for negPhrase in phrases_to_omit:
                if posPhrase in words_around_backlog and negPhrase not in words_around_backlog:
                    return 1
    return 0


###############################
# End of configuration
###############################


def get_num_phrases_in_sentences(text, matching_indices, phrases):
    count = 0
    # Don't double count 2 occurences in the same sentence
    sentences = set()
    for index in matching_indices:
        words_around_backlog = get_sentence(text, index)
        if words_around_backlog not in sentences:
            sentences.add(words_around_backlog)
            for phrase in phrases:
                count += words_around_backlog.count(phrase)

    return count
# Gets the number of phrases in the same sentence as "backlog"


def get_sentence(text, index, sentence_markers=end_of_sentence_markers):
    beginning_pointer = index
    ending_pointer = index
    while (ending_pointer < len(text) and
           text[ending_pointer] not in sentence_markers and
           text[ending_pointer: ending_pointer + 2] not in sentence_markers):
        ending_pointer += 1

    while (beginning_pointer > 0 and
           text[beginning_pointer] not in sentence_markers and
           text[beginning_pointer: beginning_pointer + 2] not in sentence_markers):
        beginning_pointer -= 1

    return text[beginning_pointer - 1: ending_pointer + 2]
# Given a blob of text and an index, extracts the sentence that the index is in


def get_closest_distance_to_phrases(text, matching_indices, chars_to_search, phrases_to_match):
    '''
    Gets the minimum distance of a phrase from backlog.
    Returns -1 if there are no mentions inside 'chars_to_search'
    '''
    closest_distance = 999
    for index in matching_indices:
        substring_beginning_index = max(0, index - chars_to_search)
        words_around_backlog = text[substring_beginning_index: min(len(text), index + chars_to_search)]
        backlog_index = index - substring_beginning_index
        for phrase in phrases_to_match:
            if phrase in words_around_backlog:
                phrase_mention_locations = [iter.start() for iter in re.finditer(phrase, words_around_backlog)]
                for phraseIndex in phrase_mention_locations:
                    curr_distance = 0
                    if backlog_index > phraseIndex:
                        curr_distance = backlog_index - phraseIndex - len(phrase)
                    else:
                        curr_distance = phraseIndex - backlog_index - len('backlog')
                    closest_distance = min(closest_distance, curr_distance)

    return closest_distance if closest_distance is not 999 else -1



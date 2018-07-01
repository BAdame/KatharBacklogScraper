import re
from output_object import OutputObject

# Punctuation defining end of sentences
end_of_sentence_markers = ["? ", "! ", ". ", ".\t", "\n", "\r", '."', ".'", u"\u2022",  # Bullet point
                           ]
end_of_sentence_markers_no_newlines = ["? ", "! ", ". ", '."', ".'", ".\t", u"\u2022",  # Bullet point
                                       ]
quantPhrasesToMatch = ["%", "$", "million", "billion", "percent", "dollars", " units", "home", "house", 'railcar',
                       "theater"]
negPhrasesToMatch = ["reduction", "decreas", "decline", "below", "lower", "down", "weak", "reduced", "negatively"]
posPhrasesToMatch = ["grow", "increas", "strong", "grew", "high", "improve", "record"]


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
                    cik=input_object.cik,
                    conf_call_filename=input_object.conf_call_filename,
                    fdate=input_object.fdate,
                    gvkey=input_object.gvkey,
                    mentioner_names = get_mentioner_names(raw_text, backlog_mention_locations) if is_transcript else ' ',
                    nblog_mention=get_n_blog_mention(raw_text, backlog_mention_locations),
                    neg_blog=get_neg_blog(raw_text, backlog_mention_locations),
                    neg_blog_dist=get_closest_distance_to_phrases(raw_text, backlog_mention_locations, 200,
                                                                  negPhrasesToMatch),
                    num_negblog=get_num_neg_blog(raw_text, backlog_mention_locations),
                    num_posblog=get_num_pos_blog(raw_text, backlog_mention_locations),
                    obfirm=input_object.obfirm,
                    pos_blog=get_pos_blog(raw_text, backlog_mention_locations),
                    pos_blog_dist=get_closest_distance_to_phrases(raw_text, backlog_mention_locations, 200,
                                                                  posPhrasesToMatch),
                    wrdsfname=input_object.wrdsfname
                )

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
    return re.sub('[\n\r\t,]', ' ', text_to_return)


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



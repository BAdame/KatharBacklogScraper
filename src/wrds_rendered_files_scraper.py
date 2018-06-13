'''
Created on May 7, 2018

@author: adameb
'''
from output_object import OutputObject
from os.path import join
import traceback
import re
from utils import getInputObjects
import time
import sys

###############################
# Begin configuration options
###############################

# The absolute path of the file to use as input.
INPUT_FILE_PATH = './inputFiles/full_input.csv' if sys.argv[1] is None else sys.argv[1]

# Punctuation defining end of sentences
endOfSentenceMarkers = ["? ", "! ", ". ", ".\t", "\n", "\r",
                        u"\u2022", # Bullet point
                        ]
quantPhrasesToMatch = ["%", "$", "million", "billion", "percent", "dollars"]
negPhrasesToMatch = ["reduction", "decreas", "decline", "below", "lower", "down", "weak", "reduced", "negatively"]
posPhrasesToMatch = ["grow", "increas", "strong", "grew", "high", "improve", "record"]

# The root folder for the data files
INPUT_FILES_ROOT_DIRECTORY = '/mnt/c/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src/textfiles'
# INPUT_FILES_ROOT_DIRECTORY = 'C:/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src/textfiles'

# The name and location of the file to print results to
OUTPUT_FILE = 'output/test-results-full-rendered.csv' if sys.argv[2] is None else sys.argv[2]

###############################
# Below are the text matching rules, which can be tweaked to produce different outputs.
###############################


# '0/1 variable: 0 if "backlog" is NOT mentioned; 1 if "backlog" is mentioned
def get_blog_mention(text, matching_indices):
    return 1 if (len(matching_indices) > 0) else 0


# 0/1 variable: 1 if ANY mention of "backlog" is within the same sentence of 
# "%", "$", "million", "billion", "percent", or "dollars"; 0 otherwise
def get_blog_quant(text, matching_indices):
    for index in matching_indices:
        words_around_backlog = get_sentence(text, index)
        for phrase in quantPhrasesToMatch:
            if phrase in words_around_backlog:
                return 1
    return 0


# Number of sentences backlog was mentioned in
# Example: if the only mentions of backlog were: 
# "Backlog sucked. Don't ask about our backlog." this would take the value of 2.
def get_blog_sent(text, matching_indices):
    sentences = set()
    for index in matching_indices:
        sentences.add(get_sentence(text, index))
        
    return len(sentences)


# shortest distance (in characters) between any mention of backlog and any of the 
# existing quantitative phrases/characters - max of 300
def get_blog_quant_dist(text, matching_indices, chars_to_search = 300):
    return get_closest_distance_to_phrases(text, matching_indices, chars_to_search, quantPhrasesToMatch)


def get_blog_quant_table(text, matching_indices, chars_to_search = 40):
    for index in matching_indices:
        text_after_backlog = text[index : index+chars_to_search]
        # Match at least 3 digits in a row, excluding commas
        number_matches = re.findall('\d{3}', text_after_backlog.replace(',', ''))
        if len(number_matches) > 0:
            return 1
    return 0


# shortest distance (in characters) between any mention of backlog
def get_blog_sh_dist(text, matching_indices, chars_to_search = 500):
    phrases_to_match = ["safe harbor", "private securities litigation reform", "forward-looking", "forward looking"]
    return get_closest_distance_to_phrases(text, matching_indices, chars_to_search, phrases_to_match)


# shortest distance (in characters) between any mention of backlog
def get_blog_surrounding_text(text, matching_indices, chars_to_search = 150):
    text_separator = '   -----------   '
    text_to_return = ''
    for index in matching_indices:
        surrounding_text = text[ max(0, index - chars_to_search) : min(len(text), index + chars_to_search) ]
        text_to_return += surrounding_text + text_separator
    return re.sub('[\n\r\t,]', ' ', text_to_return)


# number of backlog mentions
def get_n_blog_mention(text, matching_indices):
    return len(matching_indices)


# 0/1 variable: 1 if ANY mention of "backlog" is in the same sentence as of 
# any of the following terms: 
# "reduction", "decreas", "decline", "below", "lower", "down", "weak"
def get_neg_blog(text, matching_indices):
    for index in matching_indices:
        words_around_backlog = get_sentence(text, index)
        for phrase in negPhrasesToMatch:
            if phrase in words_around_backlog:
                return 1
    return 0


# Number of times a negative word was in the same sentence as backlog
def get_num_neg_blog(text, matching_indices):
    return get_num_phrases_in_sentences(text, matching_indices, negPhrasesToMatch)


# Number of times a positive word was in the same sentence as backlog
def get_num_pos_blog(text, matching_indices):
    return get_num_phrases_in_sentences(text, matching_indices, posPhrasesToMatch)


# 0/1 variable: 1 if ANY mention of "backlog" is within the same sentence of
# any of the following terms: 
# "grow", "increas", "strong", "grew", "high", "improve", "record" (but NOT "recorded")
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


# Gets the number of phrases in the same sentence as "backlog"
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


# Given a blob of text and an index, extracts the sentence that the index is in
def get_sentence(text, index):
    beginning_pointer = index
    ending_pointer = index
    while (text[ending_pointer] not in endOfSentenceMarkers and
           text[ending_pointer : ending_pointer + 2] not in endOfSentenceMarkers and
           ending_pointer < len(text)):
        ending_pointer += 1
    
    while (text[beginning_pointer] not in endOfSentenceMarkers and
            text[beginning_pointer : beginning_pointer+2] not in endOfSentenceMarkers and
            beginning_pointer > 0):
        beginning_pointer -= 1
    
    return text[beginning_pointer - 1 : ending_pointer + 2]


def get_closest_distance_to_phrases(text, matching_indices, chars_to_search, phrases_to_match):
    '''
    Gets the minimum distance of a phrase from backlog.
    Returns -1 if there are no mentions inside 'chars_to_search'
    '''
    closest_distance = 999
    for index in matching_indices:
        substring_beginning_index = max(0, index - chars_to_search)
        words_around_backlog = text[substring_beginning_index : min(len(text), index + chars_to_search)]
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

def main():
    # Read the input file into a list of objects
    input_objects = getInputObjects(INPUT_FILE_PATH)

    results_file = open(OUTPUT_FILE, 'w')
    results_file.write(OutputObject.getCsvHeaders())
    
    # For each line of input
    for inputObject in input_objects:
        # Fine the data file's full path
        full_file_path = join(INPUT_FILES_ROOT_DIRECTORY, inputObject.wrdsfname + ".rendered")
        # Hack for Windows
        if 'C:' in full_file_path:
            full_file_path = full_file_path.replace('/', '\\')
        try:
            # Open the data file
            print("Opening {}".format(full_file_path))
            with open(full_file_path, 'r') as dataFile:
                # Get the file contents as a giant blob of text, stripping all HTML tags
                data_file_raw_text = dataFile.read()

                # Some files may include 99.2 documents at the end, we want to exclude that section if so.
                n_992_mentions = [it.start() for it in re.finditer('99\.2', data_file_raw_text)]
                if len(n_992_mentions) > 0:
                    last_mention = n_992_mentions[len(n_992_mentions) - 1]
                    data_file_raw_text = data_file_raw_text[0 : last_mention]

                # Find all the locations of 'backlog' in the text
                backlog_mention_locations = [it.start() for it in re.finditer('backlog', data_file_raw_text)]

                # Do analysis
                output_object = OutputObject(
                    blog_mention = get_blog_mention(data_file_raw_text, backlog_mention_locations),
                    blog_quant = get_blog_quant(data_file_raw_text, backlog_mention_locations),
                    blog_quant_dist = get_blog_quant_dist(data_file_raw_text, backlog_mention_locations),
                    blog_quant_table = get_blog_quant_table(data_file_raw_text, backlog_mention_locations),
                    blog_sent = get_blog_sent(data_file_raw_text, backlog_mention_locations),
                    blog_sh_dist = get_blog_sh_dist(data_file_raw_text, backlog_mention_locations),
                    blog_surrounding_text = get_blog_surrounding_text(data_file_raw_text, backlog_mention_locations),
                    cik = inputObject.cik,
                    conf_call_filename = inputObject.conf_call_filename,
                    fdate = inputObject.fdate,
                    gvkey = inputObject.gvkey,
                    nblog_mention = get_n_blog_mention(data_file_raw_text, backlog_mention_locations),
                    neg_blog = get_neg_blog(data_file_raw_text, backlog_mention_locations),
                    neg_blog_dist = get_closest_distance_to_phrases(data_file_raw_text, backlog_mention_locations, 200, negPhrasesToMatch),
                    num_negblog = get_num_neg_blog(data_file_raw_text, backlog_mention_locations),
                    num_posblog = get_num_pos_blog(data_file_raw_text, backlog_mention_locations),
                    obfirm = inputObject.obfirm,
                    pos_blog = get_pos_blog(data_file_raw_text, backlog_mention_locations),
                    pos_blog_dist = get_closest_distance_to_phrases(data_file_raw_text, backlog_mention_locations, 200, posPhrasesToMatch),
                    wrdsfname = inputObject.wrdsfname
                    )

                # Write to file
                results_file.write(output_object.getCsv())
                print(output_object.getCsv())
        except Exception: 
            print("Error loading file: [[[{}]]] @@@{}@@@".format(full_file_path, inputObject.wrdsfname))
            traceback.print_exc()


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time: {}".format((time.time() - start)))

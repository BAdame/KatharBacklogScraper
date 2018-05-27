'''
Created on May 7, 2018

@author: adameb
'''
from bs4 import BeautifulSoup
from output_object import OutputObject
from input_object import InputObject
from os.path import join
import traceback
import re
from utils import getInputObjects
import time

###############################
# Begin configuration options
###############################

# The absolute path of the file to use as input.
INPUT_FILE_PATH = './full_input_just_0s.csv'

# The root folder for the data files
INPUT_FILES_ROOT_DIRECTORY = '/mnt/c/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src'
INPUT_FILES_ROOT_DIRECTORY = 'C:/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src'

# The name and location of the file to print results to
OUTPUT_FILE = 'results-0.csv'

###############################
# Below are the text matching rules, which can be tweaked to produce different outputs.
###############################

# '0/1 variable: 0 if "backlog" is NOT mentioned; 1 if "backlog" is mentioned
def getBlogMention(text, matchingIndices):
    return 1 if (len(matchingIndices) > 0) else 0

# 0/1 variable: 1 if ANY mention of "backlog" is within 100 characters of 
# "%", "$", "million", "billion", "percent", or "dollars"; 0 otherwise
def getBlogQuant(text, matchingIndices, charactersToSearch = 100):
    phrasesToMatch = ["%", "$", "million", "billion", "percent", "dollars"]
    for index in matchingIndices:
        wordsAroundBacklog = text[max(0, index - charactersToSearch) : min(len(text), index + charactersToSearch)]
        for phrase in phrasesToMatch:
            if phrase in wordsAroundBacklog:
                return 1
    return 0

# sum of the number of characters in the same sentence as any mention of backlog. 
# Example: if the only mentions of backlog were: 
# "Backlog sucked. Don't ask about our backlog." this would take the value of 44.
def getBlogSent(text, matchingIndices):
    count = 0
    punctuation = [".", "?", "!"]
    # Naive approach - Start at the mention, march forwards and backwards until ending punctuation is found.
    for index in matchingIndices:
        pointer = index
        while text[pointer] not in punctuation:
            count += 1
            pointer += 1
        
        pointer = index
        while text[pointer] not in punctuation:
            count += 1
            pointer -= 1
        
    return count

# 0/1 variable: 1 if "backlog" is mentioned in the same sentence as - 
# or within 100 characters of - one of the following phrases: 
# "safe harbor" or 
# "private securities litigation reform". 
# Note this will be 0 if blog_mention is 0
def getBlogSh(text, matchingIndices, charactersToSearch = 100):
    phrasesToMatch = ["safe harbor", "private securities litigation reform"]
    for index in matchingIndices:
        wordsAroundBacklog = text[max(0, index - charactersToSearch) : min(len(text), index + charactersToSearch)]
        for phrase in phrasesToMatch:
            if phrase in wordsAroundBacklog:
                return 1
    return 0

# number of backlog mentions
def getNBlogMention(text, matchingIndices):
    return len(matchingIndices)

# 0/1 variable: 1 if ANY mention of "backlog" is within 100 characters of 
# any of the following terms: 
# "reduction", "decreas", "decline", "below", "lower", "down", "weak"
def getNegBlog(text, matchingIndices, charactersToSearch = 100):
    phrasesToMatch = ["reduction", "decreas", "decline", "below", "lower", "down", "weak"]
    for index in matchingIndices:
        wordsAroundBacklog = text[max(0, index - charactersToSearch) : min(len(text), index + charactersToSearch)]
        for phrase in phrasesToMatch:
            if phrase in wordsAroundBacklog:
                return 1
    return 0

# 0/1 variable: 1 if ANY mention of "backlog" is within 100 characters of
# any of the following terms: 
# "grow", "increas", "strong", "grew", "high", "improve", "record" (but NOT "recorded")
def getPosBlog(text, matchingIndices, charactersToSearch = 100):
    phrasesToMatch = ["grow", "increas", "strong", "grew", "high", "improve", "record"]
    phrasesToOmit = ["recorded"]
    for index in matchingIndices:
        wordsAroundBacklog = text[max(0, index - charactersToSearch) : min(len(text), index + charactersToSearch)]
        # TODO This would exclude phrases like "records recorded", fix that
        for phrase in phrasesToMatch:
            if phrase in wordsAroundBacklog and phrase not in phrasesToOmit:
                return 1
    return 0

###############################
# End of configuration
###############################

def main():
    # Read the input file into a list of objects
    inputObjects = getInputObjects(INPUT_FILE_PATH)

    resultsFile = open(OUTPUT_FILE, 'w')
    resultsFile.write(OutputObject.getCsvHeaders())
    
    # For each line of input
    for inputObject in inputObjects:
        # Fine the data file's full path
        fullFilePath = join(INPUT_FILES_ROOT_DIRECTORY, inputObject.wrdsfname)
        # Hack for Windows
        if 'C:' in fullFilePath:
            fullFilePath = fullFilePath.replace('/', '\\')
        try:
            # Open the data file
            with open(fullFilePath, 'r') as dataFile:
                # Get the file contents as a giant blob of text, stripping all HTML tags
                dataFileHtmlText = dataFile.read()
                dataFileHtmlDomObject = BeautifulSoup(dataFileHtmlText, 'lxml');
                dataFileRawText = dataFileHtmlDomObject.get_text().lower()

                # Find all the locations of 'backlog' in the text
                backlogMentionLocations = [iter.start() for iter in re.finditer('backlog', dataFileRawText)]

                # Do analysis
                outputObject = OutputObject(
                    blog_mention = getBlogMention(dataFileRawText, backlogMentionLocations),
                    blog_quant = getBlogQuant(dataFileRawText, backlogMentionLocations),
                    blog_sh = getBlogSh(dataFileRawText, backlogMentionLocations),
                    blog_sent = getBlogSent(dataFileRawText, backlogMentionLocations),
                    cik = inputObject.cik,
                    conf_call_filename = inputObject.conf_call_filename,
                    fdate = inputObject.fdate,
                    gvkey = inputObject.gvkey,
                    nblog_mention = getNBlogMention(dataFileRawText, backlogMentionLocations),
                    neg_blog = getNegBlog(dataFileRawText, backlogMentionLocations),
                    obfirm = inputObject.obfirm,
                    pos_blog = getPosBlog(dataFileRawText, backlogMentionLocations),
                    wrdsfname = inputObject.wrdsfname
                    )
                
                # Write to file
                resultsFile.write(outputObject.getCsv())
                print(outputObject.getCsv())
        except Exception: 
            print("Error loading file: [[[{}]]] @@@{}@@@".format(fullFilePath, inputObject.wrdsfname))
            traceback.print_exc()


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time: {}".format((time.time() - start)))

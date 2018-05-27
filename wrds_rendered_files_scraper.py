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
import sys

###############################
# Begin configuration options
###############################

# The absolute path of the file to use as input.
INPUT_FILE_PATH = './full_input.csv' if sys.argv[1] is None else sys.argv[1]

# Punctuation defining end of sentences
endOfSentenceMarkers = ["? ", "! ", ". ", ".\t", "\n", "\r",
                        u"\u2022", # Bullet point
                        ]
quantPhrasesToMatch = ["%", "$", "million", "billion", "percent", "dollars"]
negPhrasesToMatch = ["down from", "reduction", "decreas", "decline", "below", "lower", "down", "weak", "reduced"]
posPhrasesToMatch = ["grow", "increas", "strong", "grew", "high", "improve", "record", "negatively"]

# The root folder for the data files
INPUT_FILES_ROOT_DIRECTORY = '/mnt/c/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src/textfiles'
# INPUT_FILES_ROOT_DIRECTORY = 'C:/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src/textfiles'

# The name and location of the file to print results to
OUTPUT_FILE = 'test-results-full-rendered.csv' if sys.argv[2] is None else sys.argv[2]

###############################
# Below are the text matching rules, which can be tweaked to produce different outputs.
###############################

# '0/1 variable: 0 if "backlog" is NOT mentioned; 1 if "backlog" is mentioned
def getBlogMention(text, matchingIndices):
    return 1 if (len(matchingIndices) > 0) else 0

# 0/1 variable: 1 if ANY mention of "backlog" is within the same sentence of 
# "%", "$", "million", "billion", "percent", or "dollars"; 0 otherwise
def getBlogQuant(text, matchingIndices):
    for index in matchingIndices:
        wordsAroundBacklog = getSentence(text, index)
        for phrase in quantPhrasesToMatch:
            if phrase in wordsAroundBacklog:
                return 1
    return 0

# Number of sentences backlog was mentioned in
# Example: if the only mentions of backlog were: 
# "Backlog sucked. Don't ask about our backlog." this would take the value of 2.
def getBlogSent(text, matchingIndices):
    sentences = set()
    for index in matchingIndices:
        sentences.add( getSentence(text, index) )
        
    return len( sentences )

# shortest distance (in characters) between any mention of backlog and any of the 
# existing quantitative phrases/characters - max of 300
def getBlogQuantDist(text, matchingIndices, charsToSearch = 300):
    return getClosestDistanceToPhrases(text, matchingIndices, charsToSearch, quantPhrasesToMatch)

# shortest distance (in characters) between any mention of backlog
def getBlogShDist(text, matchingIndices, charsToSearch = 500):
    phrasesToMatch = ["safe harbor", "private securities litigation reform", "forward-looking", "forward looking"]
    return getClosestDistanceToPhrases(text, matchingIndices, charsToSearch, phrasesToMatch)

# number of backlog mentions
def getNBlogMention(text, matchingIndices):
    return len(matchingIndices)

# 0/1 variable: 1 if ANY mention of "backlog" is in the same sentence as of 
# any of the following terms: 
# "reduction", "decreas", "decline", "below", "lower", "down", "weak"
def getNegBlog(text, matchingIndices):
    for index in matchingIndices:
        wordsAroundBacklog = getSentence(text, index)
        for phrase in negPhrasesToMatch:
            if phrase in wordsAroundBacklog:
                return 1
    return 0

# Number of times a negative word was in the same sentence as backlog
def getNumNegBlog(text, matchingIndices):
    return getNumPhrasesInSentences(text, matchingIndices, negPhrasesToMatch)

# Number of times a positive word was in the same sentence as backlog
def getNumPosBlog(text, matchingIndices):
    return getNumPhrasesInSentences(text, matchingIndices, posPhrasesToMatch)

# 0/1 variable: 1 if ANY mention of "backlog" is within the same sentence of
# any of the following terms: 
# "grow", "increas", "strong", "grew", "high", "improve", "record" (but NOT "recorded")
def getPosBlog(text, matchingIndices):
    phrasesToOmit = ["recorded"]
    for index in matchingIndices:
        wordsAroundBacklog = getSentence(text, index)
        for posPhrase in posPhrasesToMatch:
            for negPhrase in phrasesToOmit:
                if posPhrase in wordsAroundBacklog and negPhrase not in wordsAroundBacklog:
                    return 1
    return 0

###############################
# End of configuration
###############################

# Gets the number of phrases in the same sentence as "backlog"
def getNumPhrasesInSentences(text, matchingIndices, phrases):
    count = 0
    # Don't double count 2 occurences in the same sentence
    sentences = set()
    for index in matchingIndices:
        wordsAroundBacklog = getSentence(text, index)
        if wordsAroundBacklog not in sentences:
            sentences.add(wordsAroundBacklog)
            for phrase in phrases:
                count += wordsAroundBacklog.count(phrase)

    return count

# Given a blob of text and an index, extracts the sentence that the index is in
def getSentence(text, index):
    beginningPointer = index
    endingPointer = index
    while (text[endingPointer] not in endOfSentenceMarkers and 
           text[endingPointer : endingPointer + 2] not in endOfSentenceMarkers and
           endingPointer < len(text)):
        endingPointer += 1
    
    while (text[beginningPointer] not in endOfSentenceMarkers and
            text[beginningPointer : beginningPointer+2] not in endOfSentenceMarkers and
            beginningPointer > 0):
        beginningPointer -= 1
    
    return text[beginningPointer - 1 : endingPointer + 2]

def getClosestDistanceToPhrases(text, matchingIndices, charsToSearch, phrasesToMatch):
    '''
    Gets the minimum distance of a phrase from backlog.
    Returns -1 if there are no mentions inside 'charsToSearch'
    '''
    closestDistance = 999
    for index in matchingIndices:
        substringBeginningIndex = max(0, index - charsToSearch)
        wordsAroundBacklog = text[substringBeginningIndex : min(len(text), index + charsToSearch)]
        backlogIndex = index - substringBeginningIndex
        for phrase in phrasesToMatch:
            if phrase in wordsAroundBacklog:
                phraseMentionLocations = [iter.start() for iter in re.finditer(phrase, wordsAroundBacklog)]
                for phraseIndex in phraseMentionLocations:
                    currDistance = 0
                    if backlogIndex > phraseIndex:
                        currDistance = backlogIndex - phraseIndex - len(phrase)
                    else:
                        currDistance = phraseIndex - backlogIndex - len('backlog')
                    closestDistance = min(closestDistance, currDistance)
            
    return closestDistance if closestDistance is not 999 else -1

def main():
    # Read the input file into a list of objects
    inputObjects = getInputObjects(INPUT_FILE_PATH)

    resultsFile = open(OUTPUT_FILE, 'w')
    resultsFile.write(OutputObject.getCsvHeaders())
    
    # For each line of input
    for inputObject in inputObjects:
        # Fine the data file's full path
        fullFilePath = join(INPUT_FILES_ROOT_DIRECTORY, inputObject.wrdsfname + ".rendered")
        # Hack for Windows
        if 'C:' in fullFilePath:
            fullFilePath = fullFilePath.replace('/', '\\')
        try:
            # Open the data file
            with open(fullFilePath, 'r') as dataFile:
                # Get the file contents as a giant blob of text, stripping all HTML tags
                dataFileRawText = dataFile.read()

                # Find all the locations of 'backlog' in the text
                backlogMentionLocations = [iter.start() for iter in re.finditer('backlog', dataFileRawText)]

                # Do analysis
                outputObject = OutputObject(
                    blog_mention = getBlogMention(dataFileRawText, backlogMentionLocations),
                    blog_quant = getBlogQuant(dataFileRawText, backlogMentionLocations),
                    blog_quant_dist = getBlogQuantDist(dataFileRawText, backlogMentionLocations),
                    blog_sh_dist = getBlogShDist(dataFileRawText, backlogMentionLocations),
                    blog_sent = getBlogSent(dataFileRawText, backlogMentionLocations),
                    cik = inputObject.cik,
                    conf_call_filename = inputObject.conf_call_filename,
                    fdate = inputObject.fdate,
                    gvkey = inputObject.gvkey,
                    nblog_mention = getNBlogMention(dataFileRawText, backlogMentionLocations),
                    neg_blog = getNegBlog(dataFileRawText, backlogMentionLocations),
                    neg_blog_dist = getClosestDistanceToPhrases(dataFileRawText, backlogMentionLocations, 200, negPhrasesToMatch),
                    num_negblog = getNumNegBlog(dataFileRawText, backlogMentionLocations),
                    num_posblog = getNumPosBlog(dataFileRawText, backlogMentionLocations),
                    obfirm = inputObject.obfirm,
                    pos_blog = getPosBlog(dataFileRawText, backlogMentionLocations),
                    pos_blog_dist = getClosestDistanceToPhrases(dataFileRawText, backlogMentionLocations, 200, posPhrasesToMatch),
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

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
import sys
import time
from utils import getInputObjects
import os
import errno

###############################
# Begin configuration options
###############################

# The root folder for the data files
INPUT_FILES_ROOT_DIRECTORY = '/mnt/c/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src/wrds-files/wrds-files/wrds/sec/warchives/'
#INPUT_FILES_ROOT_DIRECTORY = 'C:/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src'
OUTPUT_FILES_ROOT_DIRECTORY = '/mnt/c/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src/textfiles'

def main():
    inputFile = sys.argv[1].rstrip()
    
    # Fine the data file's full path
    fullFilePath = join(INPUT_FILES_ROOT_DIRECTORY, inputFile)
    fileOutputPath = join(OUTPUT_FILES_ROOT_DIRECTORY, inputFile + ".rendered")
    
    if not os.path.exists(os.path.dirname(fileOutputPath)):
        try:
            os.makedirs(os.path.dirname(fileOutputPath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # Hack for Windows
    if 'C:' in fullFilePath:
        fullFilePath = fullFilePath.replace('/', '\\')
    try:
        # Open the data file
        with open(fullFilePath, 'r') as dataFile:
            # Get the file contents as a giant blob of text, stripping all HTML tags
            dataFileHtmlText = dataFile.read()
            
            # BS doesn't handle newlines properly, this hack seems to fix it.
            dataFileHtmlDomObject = BeautifulSoup(dataFileHtmlText, 'lxml');
            dataFileRawText = "\n".join([text.replace("\n", " ") for text in dataFileHtmlDomObject.stripped_strings])
            dataFileRawText = dataFileRawText.encode('ascii', 'ignore').decode('ascii').lower()
            
            outputFile = open(fileOutputPath, 'w')
            outputFile.write(dataFileRawText)
    except Exception: 
        print("Error loading file: [[[{}]]] @@@{}@@@".format(fullFilePath, inputFile))
        traceback.print_exc()


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time for {}: [[{}]]".format(sys.argv[1].rstrip(), (time.time() - start)))

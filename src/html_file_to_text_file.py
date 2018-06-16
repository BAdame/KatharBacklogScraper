'''
Created on May 7, 2018

@author: adameb
'''
from bs4 import BeautifulSoup
from os.path import join
from html_to_text import Renderer
import traceback
import sys
import time
import os
import errno
import re

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
    full_file_path = join(INPUT_FILES_ROOT_DIRECTORY, inputFile)
    fileOutputPath = join(OUTPUT_FILES_ROOT_DIRECTORY, inputFile + ".rendered")
    
    if not os.path.exists(os.path.dirname(fileOutputPath)):
        try:
            os.makedirs(os.path.dirname(fileOutputPath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # Hack for Windows
    if 'C:' in full_file_path:
        full_file_path = full_file_path.replace('/', '\\')
    try:
        # Open the data file
        with open(full_file_path, 'r') as dataFile:
            # Get the file contents as a giant blob of text, stripping all HTML tags
            data_file_html_text = dataFile.read()

            # Graphics cause the markdown renderer to barf, omit those
            graphic_locations = [i.start() for i in re.finditer('<TYPE>GRAPHIC', data_file_html_text)]
            if len(graphic_locations) > 0:
                # Omit everything after the first graphic
                data_file_html_text = data_file_html_text[0 : graphic_locations[0]]

            # data_file_raw_text = data_file_raw_text.encode('ascii', 'ignore').decode('ascii').lower()
            data_file_raw_text = Renderer().html_to_text_h2t(data_file_html_text)\
                .encode('ascii', 'ignore').decode('ascii').lower()

            output_file = open(fileOutputPath, 'w')
            output_file.write(data_file_raw_text)
    except Exception: 
        print("Error loading file: [[[{}]]] @@@{}@@@".format(full_file_path, inputFile))
        traceback.print_exc()


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time for {}: [[{}]]".format(sys.argv[1].rstrip(), (time.time() - start)))

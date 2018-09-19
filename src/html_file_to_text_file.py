'''
Created on May 7, 2018

@author: adameb
'''
import codecs
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
INPUT_FILES_ROOT_DIRECTORY = '/mnt/c/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src/4000-wrds-files/'
# INPUT_FILES_ROOT_DIRECTORY = 'C:/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src'
OUTPUT_FILES_ROOT_DIRECTORY = '/mnt/c/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src/textfiles'


def main():
    input_file = sys.argv[1].rstrip()

    # Fine the data file's full path
    full_file_path = join(INPUT_FILES_ROOT_DIRECTORY, input_file)
    file_output_path = join(OUTPUT_FILES_ROOT_DIRECTORY, input_file + ".rendered")

    if not os.path.exists(os.path.dirname(file_output_path)):
        try:
            os.makedirs(os.path.dirname(file_output_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # Hack for Windows
    if 'C:' in full_file_path:
        full_file_path = full_file_path.replace('/', '\\')
   # try:
        # Open the data file
    with codecs.open(full_file_path, 'r', 'utf-8') as dataFile:
        # Get the file contents as a giant blob of text, stripping all HTML tags
        data_file_html_text = dataFile.read()

        data_file_html_text = remove_content_block_by_type(data_file_html_text, 'EXCEL')
        data_file_html_text = remove_content_block_by_type(data_file_html_text, 'GRAPHIC')
        data_file_html_text = remove_content_block_by_type(data_file_html_text, 'EX-99.2')
        data_file_html_text = remove_content_block_by_element(data_file_html_text, 'PDF')
        data_file_html_text = remove_content_block_by_element(data_file_html_text, 'XBRL')
        data_file_html_text = remove_content_block_by_type(data_file_html_text, 'XML')
        data_file_html_text = remove_content_block_by_type(data_file_html_text, 'ZIP')

        # Graphics contain invalid HTML, try to remove that
        data_file_html_text = data_file_html_text.replace('<!', ' ')

        data_file_raw_text = Renderer().html_to_text_h2t(data_file_html_text) \
            .encode('ascii', 'ignore').decode('ascii').lower()

        output_file = open(file_output_path, 'w')
        output_file.write(data_file_raw_text)
   # except Exception:
     #   print("Error loading file: [[[{}]]] @@@{}@@@".format(full_file_path, input_file))
      #  traceback.print_exc()


def remove_content_block_by_element(text, element):
    '''
    Removes text in this format:
    <TYPE>${type}
    ...content
    <element>
    ....content
    </element>
    '''
    # Get the number of mentions of the tag
    beginning_tag = '<{}>'.format(element)
    end_tag = '</{}>'.format(element)
    mentions = re.findall(beginning_tag, text)

    # Don't iterate of the list of mentions since text gets removed, indices change
    for i in range(len(mentions)):
        print('removing tag ' + beginning_tag)
        # Find index of the first tag
        block_beginning = text.find(beginning_tag)

        # Find closing </element> element after the tag
        block_end = text[block_beginning:].find(end_tag) + block_beginning

        # Remove text
        text = text[0: block_beginning] + text[block_end + len(end_tag):]
    return text


def remove_content_block_by_type(text, type):
    '''
    Removes text in this format:
    <TYPE>${type}
    ...content
    <TEXT>
    ....content
    </TEXT>
    '''
    # Get the number of mentions of the tag
    beginning_tag = '<TYPE>{}'.format(type)
    end_tag = '</TEXT>'
    mentions = re.findall(beginning_tag, text)

    # Don't iterate of the list of mentions since text gets removed, indices change
    for i in range(len(mentions)):
        print('removing tag ' + beginning_tag)
        # Find index of the first tag
        block_beginning = text.find(beginning_tag)

        # Find closes </TEXT> element after the tag
        block_end = text[block_beginning:].find(end_tag) + block_beginning

        # Remove text
        text = text[0: block_beginning] + text[block_end + len(end_tag):]
    return text


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time for {}: [[{}]]".format(sys.argv[1].rstrip(), (time.time() - start)))

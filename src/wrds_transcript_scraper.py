"""
Created on May 7, 2018

@author: adameb
"""
from output_object import OutputObject
from os.path import join
import traceback
import re
from utils import get_input_objects
import time
import sys
from analyzing_rules import get_output_object

###############################
# Begin configuration options
###############################

# The absolute path of the file to use as input.
INPUT_FILE_PATH = './inputFiles/full_input.csv' if len(sys.argv) <= 1 else sys.argv[1]

# The root folder for the data files
# TODO Take this as input
INPUT_FILES_ROOT_DIRECTORY = './inputFiles/transcripts'

# The name and location of the file to print results to
OUTPUT_FILE = 'output/test-results-full-rendered.csv' if len(sys.argv) <= 2 else sys.argv[2]


###############################
# Below are the text matching rules, which can be tweaked to produce different outputs.
###############################


def main():
    # Read the input file into a list of objects
    input_objects = get_input_objects(INPUT_FILE_PATH)

    results_file = open(OUTPUT_FILE, 'w')
    results_file.write(OutputObject.get_csv_headers())

    # For each line of input
    for input_object in input_objects:
        # Not all entries have a transcript
        if not input_object.conf_call_filename:
            continue
        # Fine the data file's full path
        full_file_path = join(INPUT_FILES_ROOT_DIRECTORY, input_object.conf_call_filename)
        try:
            # Open the data file
            print("Opening {}".format(full_file_path))
            with open(full_file_path, 'r') as dataFile:
                # Get the file contents as a giant blob of text, stripping all HTML tags
                data_file_raw_text = dataFile.read().lower()

                # Do analysis
                output_object = get_output_object(input_object, data_file_raw_text, is_transcript=True)

                # Write to file
                results_file.write(output_object.get_csv())
                print(output_object.get_csv())
        except Exception:
            print("Error loading file: [[[{}]]] @@@{}@@@".format(full_file_path, input_object.wrdsfname))
            traceback.print_exc()


if __name__ == '__main__':
    start = time.time()
    main()
    print("Total time: {}".format((time.time() - start)))

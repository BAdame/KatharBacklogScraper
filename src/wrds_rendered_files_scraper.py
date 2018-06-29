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
import analyzing_rules

###############################
# Begin configuration options
###############################

# The absolute path of the file to use as input.
INPUT_FILE_PATH = './inputFiles/full_input.csv' if len(sys.argv) <= 1 else sys.argv[1]

# The root folder for the data files
INPUT_FILES_ROOT_DIRECTORY = '/mnt/c/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src/textfiles'
# INPUT_FILES_ROOT_DIRECTORY = 'C:/Users/adameb/eclipseworkspace/KatharSarahProject/wrds-scraper-src/textfiles'

# The name and location of the file to print results to
OUTPUT_FILE = 'output/test-results-full-rendered.csv' if len(sys.argv) <= 2 else sys.argv[2]


###############################
# Below are the text matching rules, which can be tweaked to produce different outputs.
###############################

# 0/1 variable: 1 if ANY mention of "backlog" is within the same sentence of
# any of the following terms:
# "grow", "increas", "strong", "grew", "high", "improve", "record" (but NOT "recorded")

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

                # Replace empty table cells
                data_file_raw_text = data_file_raw_text.replace('|', ' ')
                data_file_raw_text = re.sub('\s+', ' ', data_file_raw_text)
                data_file_raw_text = re.sub('\n+', '\n', data_file_raw_text)

                # Find all the locations of 'backlog' in the text
                backlog_mention_locations = [it.start() for it in re.finditer('backlog', data_file_raw_text)]

                # Do analysis
                output_object = OutputObject(
                    amor_blog_mention=analyzing_rules.get_amor_blog_mention(data_file_raw_text, backlog_mention_locations),
                    blog_mention=analyzing_rules.get_blog_mention(data_file_raw_text, backlog_mention_locations),
                    blog_quant=analyzing_rules.get_blog_quant(data_file_raw_text, backlog_mention_locations),
                    blog_quant_dist=analyzing_rules.get_blog_quant_dist(data_file_raw_text, backlog_mention_locations),
                    blog_quant_no_newlines=analyzing_rules.get_blog_quant_no_newlines(data_file_raw_text, backlog_mention_locations),
                    blog_quant_table=analyzing_rules.get_blog_quant_table(data_file_raw_text, backlog_mention_locations),
                    blog_sent=analyzing_rules.get_blog_sent(data_file_raw_text, backlog_mention_locations),
                    blog_sh_dist=analyzing_rules.get_blog_sh_dist(data_file_raw_text, backlog_mention_locations),
                    blog_surrounding_text=analyzing_rules.get_blog_surrounding_text(data_file_raw_text, backlog_mention_locations),
                    cik=inputObject.cik,
                    conf_call_filename=inputObject.conf_call_filename,
                    fdate=inputObject.fdate,
                    gvkey=inputObject.gvkey,
                    nblog_mention=analyzing_rules.get_n_blog_mention(data_file_raw_text, backlog_mention_locations),
                    neg_blog=analyzing_rules.get_neg_blog(data_file_raw_text, backlog_mention_locations),
                    neg_blog_dist=analyzing_rules.get_closest_distance_to_phrases(data_file_raw_text, backlog_mention_locations, 200,
                                                                                  analyzing_rules.negPhrasesToMatch),
                    num_negblog=analyzing_rules.get_num_neg_blog(data_file_raw_text, backlog_mention_locations),
                    num_posblog=analyzing_rules.get_num_pos_blog(data_file_raw_text, backlog_mention_locations),
                    obfirm=inputObject.obfirm,
                    pos_blog=analyzing_rules.get_pos_blog(data_file_raw_text, backlog_mention_locations),
                    pos_blog_dist=analyzing_rules.get_closest_distance_to_phrases(data_file_raw_text, backlog_mention_locations, 200,
                                                                                  analyzing_rules.posPhrasesToMatch),
                    wrdsfname=inputObject.wrdsfname
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

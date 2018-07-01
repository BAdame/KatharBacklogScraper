from input_object import InputObject

'''
Transform a CSV into InputObjects. 
This assumes the first row of the file is header names, and every row after that is data.
'''
def get_input_objects(inputFilePath):
    input_objects = []
    column_mappings = {}
    with open(inputFilePath, 'r') as inputFile:
        # Map column names to column numbers, so data can be looked up by column number
        headers = inputFile.readline().split(',')
        print(headers)
        for i in range(len(headers)):
            column_mappings[headers[i].replace('\n', '').replace('\r', '')] = i
            
        # Turn each row of the CSV into an object
        for row in inputFile:
            values = row.rstrip().replace('\n', '').split(',')
            input_objects.append(
                InputObject(
                    cik=values[column_mappings['cik']],
                    conf_call_filename=values[column_mappings['conf_call_filename']],
                    fdate=values[column_mappings['fdate']],
                    gvkey=values[column_mappings['gvkey']],
                    obfirm=values[column_mappings['obfirm']],
                    wrdsfname=values[column_mappings['wrdsfname']]
            ))
        
    return input_objects
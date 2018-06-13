from input_object import InputObject

'''
Transform a CSV into InputObjects. 
This assumes the first row of the file is header names, and every row after that is data.
'''
def getInputObjects(inputFilePath):
    inputObjects = []
    columnMappings = {}
    with open(inputFilePath, 'r') as inputFile:
        # Map column names to column numbers, so data can be looked up by column number
        headers = inputFile.readline().split(',')
        print(headers)
        for i in range(len(headers)):
            columnMappings[headers[i].replace('\n', '').replace('\r', '')] = i
            
        # Turn each row of the CSV into an object
        for row in inputFile:
            values = row.rstrip().replace('\n', '').split(',')
            inputObjects.append(
                InputObject(
                    cik=values[columnMappings['cik']],
                    conf_call_filename=values[columnMappings['conf_call_filename']],
                    fdate=values[columnMappings['fdate']],
                    gvkey=values[columnMappings['gvkey']],
                    obfirm=values[columnMappings['obfirm']],
                    wrdsfname=values[columnMappings['wrdsfname']]
            ))
        
    return inputObjects

'''

'''
def getOutputObject(inputObject, dataFileContents):
    dataFileContents = dataFileContents.lower()
    blog_mention = None
    blog_quant = None
    blog_sh = None
    blog_sent = None
    nblog_mentions = None
    neg_blog = None
    pos_blog = None
    
    return OutputObject(
        blog_sh = blog_sh,
        blog_mention = blog_mention,
        blog_quant = blog_quant,
        blog_sent = blog_sent,
        cik = inputObject.cik,
        conf_call_filename = inputObject.conf_call_filename,
        fdate = inputObject.fdate,
        gvkey = inputObject.gvkey,
        neg_blog = neg_blog,
        obfirm = inputObject.obfirm,
        pos_blog = pos_blog,
        wrdsfname = inputObject.wrdsfname
        )
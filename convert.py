import csv
from sys import argv
import os

class TabProcessor:
    def __init__(self, stream, delimiter='\t', quotes='"', header_row=1):
        source = open(stream, 'r')


def xmloutput(source):
    header = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<accessionRecords xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
"""
    footer = "</accessionRecords>"
    basicdata = """
<record>
<accessionNumber>
<part1>%(part1)s</part1>
<part2>%(part2)s</part2>
<part3>%(part3)s</part3>
</accessionNumber>
<accessionDate>%(accessionDate)s</accessionDate>
<acquisitionType>%(acquisitionType)s</acquisitionType>
<userDefinedReal1>%(userDefinedReal1)s</userDefinedReal1>
<extentNumber>%(extentNumber)s</extentNumber>
<extentType>%(extentType)s</extentType>
<description>%(description)s</description>
<cataloged>%(cataloged)s</cataloged>
"""
    personName = """
<nameLink>
<nameLinkFunction>Source</nameLinkFunction>
<name>
<nameType>Person</nameType>
<personalPrimaryName></personalPrimaryName>
<personalRestOfName></personalRestOfName>
<personalPrefix></personalPrefix>
<personalSuffix></personalSuffix>
</name>
</nameLink>
</record>"""
    corportateName = """
<nameLink>
<nameLinkFunction>%(nameLinkFunction)s</nameLinkFunction>
<name>
<nameType>%(nameType)s</nameType>
<corporatePrimaryName>%(corporatePrimaryName)s</corporatePrimaryName>
<corporateSubordinate1>%(corporateSubordinate1)s</corporateSubordinate1>
<corporateSubordinate2>%(corporateSubordinate2)s</corporateSubordinate2>
</name>
</nameLink>
</record>"""

    sourceReader = csv.DictReader(open(source, 'r'), delimiter="\t", quotechar='"')
    output = open(os.path.splitext(source)[0] + '.xml', 'w')
    stream = ''
    stream += header
    for row in sourceReader:
        stream += basicdata % row
        if row['nameType'] == 'Corporate Body':
            stream += corportateName % row
        elif row['nameType'] == 'Person':
            stream += personName % row
    stream += footer
    output.write(stream)
    output.close()





if argv[1] == '*':
    try:
        os.mkdir('completed')
    except WindowsError:
        pass
    filelist = [x for x in os.listdir('.') if os.path.splitext(x)[1] == '.tab']
    for tabfile in filelist:
        xmloutput(tabfile)
        os.rename(tabfile, 'completed/'+tabfile)
else:
    try:
        os.mkdir('completed')
    except WindowsError:
        pass
    for tabfile in argv[1:]:
        xmloutput(tabfile)
        os.rename(tabfile, 'completed/'+tabfile)
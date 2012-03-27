import csv
from sys import argv
import os

def dataprep(row):
    """
== basicData ==
 0 -> part1
 1 -> part2
 2 -> part3
 3 -> accessionDate
 4 -> acquisitionType
 5 -> userDefinedReal1
 6 -> extentNumber
 7 -> extentType
 8 -> description
 9 -> cataloged
10 -> nameLinkFunction
== corporateName1 ==
11 -> nameType
12 -> corporatePrimaryName
13 -> corporateSubordinate1
14 -> corporateSubordinate2
== corporateName2 ==
15 -> nameType
16 -> corporatePrimaryName
== personName1 ==
17 -> nameType
18 -> personalPrimaryName
19 -> personalRestOfName
20 -> personalPrefix
21 -> personalSuffix
== personName2 ==
22 -> nameType
23 -> personalPrimaryName
24 -> personalRestOfName
25 -> personalPrefix
26 -> personalSuffix
"""
    header = ('part1', 'part2', 'part3', 'accessionDate', 'acquisitionType', 'userDefinedReal1',
        'extentNumber', 'extentType', 'title', 'description', 'cataloged', 'nameLinkFunction', 'nameType',
        'corporatePrimaryName', 'corporateSubordinate1', 'corporateSubordinate2', 'nameType', 'corporatePrimaryName',
        'nameType', 'personalPrimaryName', 'personalRestOfName', 'personalPrefix', 'personalSuffix',
        'nameType', 'personalPrimaryName', 'personalRestOfName', 'personalPrefix', 'personalSuffix')

    basicData = dict(zip(header[0:12], row[0:12]))
    if "$" in basicData['userDefinedReal1']: basicData['userDefinedReal1'] = basicData['userDefinedReal1'].replace('$', '')
    basicData['cataloged'] = basicData['cataloged'].lower()
    corportateName1 = dict(zip(header[12:16], row[12:16]))
    corportateName2 = dict(zip(header[16:18], row[16:18]))
    personName1 = dict(zip(header[18:23], row[18:23]))
    personName2 = dict(zip(header[23:], row[23:]))
    data = {'basicData':basicData, 'corportateName1':corportateName1, 'corportateName2':corportateName2,
            'personName1':personName1, 'personName2':personName2}
    return data

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
<title>%(title)s</title>
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
<personalPrimaryName>%(personalPrimaryName)s</personalPrimaryName>
<personalRestOfName>%(personalRestOfName)s</personalRestOfName>
<personalPrefix>%(personalPrefix)s</personalPrefix>
<personalSuffix>%(personalSuffix)s</personalSuffix>
</name>
</nameLink>"""
    corportateName1 = """
<nameLink>
<nameLinkFunction>Source</nameLinkFunction>
<name>
<nameType>%(nameType)s</nameType>
<corporatePrimaryName>%(corporatePrimaryName)s</corporatePrimaryName>
<corporateSubordinate1>%(corporateSubordinate1)s</corporateSubordinate1>
<corporateSubordinate2>%(corporateSubordinate2)s</corporateSubordinate2>
</name>
</nameLink>"""
    corportateName2 = """
<nameLink>
<nameLinkFunction>Source</nameLinkFunction>
<name>
<nameType>%(nameType)s</nameType>
<corporatePrimaryName>%(corporatePrimaryName)s</corporatePrimaryName>
<corporateSubordinate1></corporateSubordinate1>
<corporateSubordinate2></corporateSubordinate2>
</name>
</nameLink>"""

    sourceReader = csv.reader(open(source, 'r'), delimiter="\t", quotechar='"')
    output = open(os.path.splitext(source)[0] + '.xml', 'w')
    stream = ''
    stream += header
    sourceReader.next() # skips header row.
    for row in sourceReader:
        data = dataprep(row)
        stream += basicdata % data['basicData']
        if data['corportateName1']['nameType']:
            stream += corportateName1 % data['corportateName1']
        if data['corportateName2']['nameType']:
            stream += corportateName2 % data['corportateName2']
        if data['personName1']['nameType']:
            stream += personName % data['personName1']
        if data['personName2']['nameType']:
            stream += personName % data['personName2']
        stream += '</record>\n'
    stream += footer
    output.write(stream)
    output.close()





if argv[1] == '*':
    try:
        os.mkdir('completed')
    except OSError:
        pass
    filelist = [x for x in os.listdir('.') if os.path.splitext(x)[1] == '.tab']
    for tabfile in filelist:
        xmloutput(tabfile)
        os.rename(tabfile, 'completed/'+tabfile)
else:
    try:
        os.mkdir('completed')
    except OSError:
        pass
    for tabfile in argv[1:]:
        xmloutput(tabfile)
        os.rename(tabfile, 'completed/'+tabfile)
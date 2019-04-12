import xml.etree.ElementTree as ET
import os

PHENOMENA = ['ABDOMINAL',
             'ADVANCED-CAD',
             'ALCOHOL-ABUSE',
             'ASP-FOR-MI',
             'CREATININE',
             'DIETSUPP-2MOS',
             'DRUG-ABUSE',
             'ENGLISH',
             'HBA1C',
             'KETO-1YR',
             'MAJOR-DIABETES',
             'MAKES-DECISIONS', 
             'MI-6MOS']

FILE = 'File'

with open('testLabels.csv', 'w') as csvf:

    csvf.write(FILE)
    for p in PHENOMENA:
        csvf.write(',' + p)
    csvf.write('\n')

    for name in sorted(n for n in os.listdir('test') if not n.startswith('.')):
        fullname = os.path.join('test', name)
        num = name.split('.')[0]

        tree = ET.parse(fullname)
        root = tree.getroot()
        tags = root.find('TAGS')

        tagdict = {}
        for x in tags:
            tagdict[x.tag] = x.get('met')
            if x.tag not in PHENOMENA:
                print('tag: ', x.tag, 'not in PHENOMENA list')

        csvf.write(num)
        for p in PHENOMENA:
            csvf.write(',' + tagdict[p])
        csvf.write('\n')
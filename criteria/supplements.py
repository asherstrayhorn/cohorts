import xml.etree.ElementTree as ET
import re
from datetime import datetime
import datetime as dt
import csv
import os
import xlrd

section_headers = ['labs/studies']
ingredient = []
category = []
diet = []
dietfile = open('resource/diet_supp_list3.csv','r').readlines()  # make sure this is in same direc
for i in dietfile:
    strip = i.strip()
    if strip in ['tea', 'sage', 'noni', 'supplement', 'supplements']:
        diet.append(' ' + strip + ' ')
    else:
        diet.append(strip)

def month_diff(date1,date2):
    if date1 > date2:
        date1,date2=date2,date1
    m1 = date1.year * 12 + date1.month
    m2 = date2.year * 12 + date2.month
    months = m2 - m1
    if date1.day > date2.day:
        months -= 1
    elif date1.day == date2.day:     # ummmm now if date1.second - date2.second > date2.minute - date1.minute , may cause error
        seconds1 = date1.hour * 3600 + date1.minute + date1.second
        seconds2 = date2.hour * 3600 + date2.minute + date2.second
        if seconds1 > seconds2:
            months -= 1
    return months

def most_recent_files(med_text):
    """
    find all of the records from within 2 months of the most recent record
    """
    files = []  
    record_date = re.findall(r'Record date: [0-9\-]+',med_text)  # finding <number followed by dash> concat: 5-1-8- ???
    record_date = [item.split()[2] for item in record_date]
    for i in med_text.split('****************************************************************************************************'):
        if i.strip() != '':
            files.append(i.strip())

    num = 0
    med_records = zip(record_date,files)
    med_records = [(x,y) for x,y in med_records]
    med_records.sort(key=lambda x:x[0], reverse=True)
    #for i in range(1, len(med_records)): # yay        <--------- looks better
    for i in range(len(med_records))[1:]:
        date1 = dt.datetime.strptime(med_records[0][0], '%Y-%m-%d')
        date2 = dt.datetime.strptime(med_records[i][0], '%Y-%m-%d')
        if month_diff(date1,date2) < 2:
            num = i
        else:
            break

    recent_med_records = []
    for i in range(num + 1):
        recent_med_records.append(med_records[i][1].lower())
    return recent_med_records


def supp(ini_text):
    """
    split is the set of records split
    if any of the supplement words are mentioned anywhere other than (presumably) the labs, recs, chem, or exam sections,
    then condition is considered met
    """
    condition = False
    listwords = []
    recent_text = most_recent_files(ini_text)
    for text in recent_text:
        text = text.replace("a/p:","assessment/plan:")
        topics = re.findall(r'[A-Za-z/ ]{4,}:', text)
        mednotes = text
        for t in topics:
            mednotes = mednotes.replace(t, '-----SPLIT_HERE-----\n'+t)
        temp = []
        for k in mednotes.split('-----SPLIT_HERE-----\n'):
            if 'labs' in k or 'labs and studies:' in k or 'labs/studies:' in k:
                continue
            elif 'recommendations:' in k:
                continue
            elif 'chemistry:' in k or 'chemistries:' in k:
                continue
            elif 'physical exam:' in k:
                continue
            else:
                temp.append(k)
        medsummary = ''.join(temp)

        # medsummary now holds in order concat of sequences of letters /s and spaces that don't contain the above search strings

        for d in diet:
            if d in medsummary:
                listwords.append(d)

        # looks like as soon as above conditions are met once, the decision is made
    if len(listwords) != 0:
        return 'met'
    else:
        return 'not met'

def proc():
    tcount = 0      # total count
    cbothmet = 0    # how many examples
    cminemet = 0    # met each criteria set
    ctheirsmet = 0  # 
    cnonemet = 0    # or met none

    condition = open('trainLabels.csv').readlines()

    # use train labels file to find files to process and the results to compare to in one place

    for row in condition[1:-3]:
        filename = row.split(",")[0]

        tree = ET.parse('./train/'+ filename +'.xml')
        root = tree.getroot()
        for child in root:
            if len(child.text) != 1:
                result = supp(filename, child.text)


                # metrics stuff   keep around to get ideas
                if row.split(",")[6] == 'met' and result[1] == "not met":
                    print(filename, result[0])
                    ctheirsmet += 1
                    tcount += 1
                if row.split(",")[6] == 'met' and result[1] == "met":
                    print(filename, result[0])
                    cbothmet += 1
                    tcount += 1
                if row.split(",")[6] == 'not met' and result[1] == "not met":
                    print(filename, result[0])
                    cnonemet += 1
                    tcount += 1
                if row.split(",")[6] == 'not met' and result[1] == "met":
                    print(filename, result[0])
                    cminemet += 1
                    tcount += 1

    print('cbothmet---------', cbothmet)
    print('cminemet---------',cminemet)
    print('ctheirsmet---------',ctheirsmet)
    print('cnonemet----------',cnonemet)
    print(tcount)
            
    """
    currently just calculating performance measures (kind of indirectly)

    However, output into is returned by supp()
    """




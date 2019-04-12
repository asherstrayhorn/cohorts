import csv
import glob
import re
import nltk
from datetime import datetime
from datetime import timedelta
import pandas as pd

#l=['STEMI','NSTEMI', 'non-ST elevation MI','RCA','Troponin','myocardial infarction','MI']
l=['STEMI','NSTEMI', 'non-ST elevation MI', 'cardiac troponin','myocardial infarction', 'stent RCA','occlusion of RCA','stenosis at the stent on the LAD','sinus with ST']
neg=['history','past','not', 'rule out','post','demand', 'no','phmx','sister','prior','father','s/p']
met=[]
file='C:/Users/1/Desktop/UM_MHI/LHS 712/n2c2/train/204.xml'

def mi6(content):
    condition='not met'    
    line=content.rstrip()
    match=re.findall(r'Record date: [0-9\-]+', line)
    most_recent=match[-1]
    most_d=datetime.strptime(most_recent[13:], '%Y-%m-%d')
    six_mon= most_d-timedelta(weeks=26, days=1)
    text_l=content.split('****************************************************************************************************')
    for date in match:
        d1=datetime.strptime(date[13:], '%Y-%m-%d')
        stop = False
        if d1 >= six_mon:           
            d2=d1.strftime('%Y-%m-%d')
            for text in text_l:
                if d2 in text:
                    sentences=text.rstrip("\n").split('.')
                    for e in sentences:
                        t= nltk.word_tokenize(e)
                        if len(t) >=3:
                            key_string=" ".join(t)

                            
                            for key in l:
                                if key_string.find(key)==-1:
                                    continue
                                else:
                                    position=key_string.index(key)
                                    
                                    if position-41>=0:
                                        key_string1=key_string[position-41:position]
                                        key_string1=key_string1.lower()
                                        
                                        for n in neg:
                                            if key_string1.find(n)==-1:
                                                continue
                                            else:
                                                stop = True
                                                return 'not met'
                                        if not stop:                                    
                                            return 'met'
                                    else:
                                        key_string1=key_string[:position]
                                        key_string1=key_string1.lower()

                                        for n in neg:
                                            if key_string1.find(n)==-1:
                                                continue
                                            elif not stop:
                                                stop = True
                                                return 'not met'
                                        if not stop:
                                            stop = True                                     
                                            return 'met'
                        else:
                            continue
                else:
                    continue
    if not stop:
        return condition                                                             

def proc():
    print(mi6(file)) 

    for file in glob.glob('C:/Users/1/Desktop/UM_MHI/LHS 712/n2c2/train/*.xml'):
        (met.append(mi6(file)))

    import os
    arr=os.listdir(path='C:/Users/1/Desktop/UM_MHI/LHS 712/n2c2/train')
    with open('C:/Users/1/Desktop/UM_MHI/LHS 712/n2c2/train1111.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("Filename", "Label"))
        wr.writerows(zip(arr,met))


import re
import os
from datetime import datetime


negative_dictionary={}
keto_dictionary={}
date_dictionary={}
flist=['(keto-*acidosis)', '(anion gap metabolic acidosis)', '(DKA)']
            
def keto(content):
    negs = []
    ketos = []
    dates = []

    for lin in content.split('\n'):
        if re.findall(r'neg_list',lin):
            for x in flist:
                nn = re.search(x,lin)
                if nn:
                    negs.append(nn.group(1))

        cc=re.search(r'(Record date:\s)(\d{4}-\d{2}-\d{2})',lin)
        if cc:
            cd=datetime.strptime(cc.group(2), '%Y-%m-%d')
        
        if re.findall(r'mappings',lin):
            for y in flist:
                kk= re.search(y,lin)
                if kk:
                    if not ketos:
                        ketos.append(( cd,kk.group(1)))
                    if ketos:
                        if cd> ketos[0][0]:
                            ketos.remove[0]
                            ketos.append(( cd,kk.group(1)))     



        if cc:
            dates.append(datetime.strptime(cc.group(2), '%Y-%m-%d'))


    dates.sort()

    if not ketos:
        return 'not met'

    elif negs:
        return 'not met'

    else:
            i=dates.index(ketos[0][0])
            if i == (len(dates)-1):
                return 'met'

            if (dates[-1]-dates[i]).days>365:
                return 'not met'

            if (dates[-1]-dates[i]).days<365:
                return 'met'






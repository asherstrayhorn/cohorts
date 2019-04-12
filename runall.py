import xml.etree.ElementTree as ET
import re, sys, os, csv, glob
import pandas as pd
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer

from criteria.alcohol import alc
from criteria.abdominal import abd
from criteria.cr_hb import creatinine, hba1c
from criteria.keto1 import keto
from criteria.mi_6mos import mi6
from criteria.supplements import supp
from criteria.drugs import drug
from criteria.makes_decisions import makes_decisions
from criteria.aspformi import asp
from criteria.smoking import smoke
from criteria.english import eng

phenomena = [alc, abd, creatinine, hba1c, keto, mi6, supp, drug, asp]
file_first = [creatinine, hba1c]


PHENOMENA = ['ALCOHOL-ABUSE',
             'ABDOMINAL',
             #'ADVANCED-CAD',
             'ASP-FOR-MI',
             'CREATININE',
             'DRUG-ABUSE',
             'DIETSUPP-2MOS',
             'ENGLISH',
             'HBA1C',
             'KETO-1YR',
             #'MAJOR-DIABETES',
             'MAKES-DECISIONS',
             'MI-6MOS']
RESULT_NEEDED = ['', 'ENGLISH']


def create_file_list(dir):
    return sorted(l for l in os.listdir(dir) if not l.startswith('.'))

#    to discover labels if needed some time    # df with true labels for each category for each file
#    ground = pd.read_csv('resource/' + directory_in + '_Labels.csv')
#    ground.index = ground['File']

def main(argv):
    # argv[1] is directory with xmls to be processed
    directory_in = argv[1]
    directory_out = 'test-out' if directory_in == 'UMich-submit2' else directory_in + '-out'
    output_file = open(directory_in + '.csv', 'w')
    output_file.write(','.join(RESULT_NEEDED))
    f_list = create_file_list(directory_in)

    # process each file in the given directory and put results in 
    # a file of the same name in an output directory
    for name in f_list:
        in_name = os.path.join(directory_in, name)
        outname = os.path.join(directory_out, name)

        # content is the preprocessed text of the actual medical report
        # tree is an ElementTree object containing the entire xml file
        content, tree = get_text(in_name)
        tags = tree.find('TAGS')
        if tags is None:
            root = tree.getroot()
            ET.SubElement(root, 'TAGS')
            tags = tree.find('TAGS')

        output_file.write('\n' + name[:-4])
        for p in PHENOMENA:
            # process file for each phenomenon in the list above
            result = do_search(p, content)
            e = tags.find(p)
            if e is None:
                ET.SubElement(tags, p)
                e = tags.find(p)
            # save the result in the tree
            e.attrib['met'] = result
            if p in RESULT_NEEDED:
                output_file.write(',' + result)

        # write the new tree to the output file
        tree.write(outname)
    output_file.close()
        
def unified_subs(content):
    content = re.sub(r"&#8211;","--", content)
    #content = content
    content = re.sub(r'&#8217;',"'", content)
    return content


def get_text(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    gen = root.findall('TEXT')
    c = 0
    for t in gen:
        if c > 0:
            print('\n\nLOOKOUT\n\n')
        else:
             res = t.text
        c += 1
    return unified_subs(res), tree

def do_search(phenomenon, content):
    # preprocess to clean character (endash)
    if phenomenon in ['alcohol', 'alcohol-abuse', 'ALCOHOL-ABUSE']:
        return alc(content)
    elif phenomenon in ['abdominal', 'ABDOMINAL']:
        return abd(content)
    elif phenomenon in ['asp', 'asp_for_mi', 'ASP-FOR-MI']:
        return asp(content)
    elif phenomenon in ['creatinine', 'CREATININE']:
        return creatinine(content)
    elif phenomenon in ['diabetes', 'major_diabetes', 'major-diabetes', 'MAJOR-DIABETES']:  # nope
        return '' # diabetes(content)
    elif phenomenon in ['dietsupp_2mos', 'DIETSUPP-2MOS']:
        return supp(content)
    elif phenomenon in ['drugs', 'drug_abuse', 'DRUG-ABUSE']:
        return drug(content)
    elif phenomenon in ['english', 'ENGLISH']:                                          
        return eng(content)
    elif phenomenon in ['hba1c', 'HBA1C']:
        return hba1c(content)
    elif phenomenon in ['keto', 'keto_1yr', 'KETO-1YR']:
        return keto(content)
    elif phenomenon in ['makes_decisions', 'MAKES-DECISIONS']:                         
        return makes_decisions(content)
    elif phenomenon in ['mi_6mo', 'MI-6MOS']:
        return mi6(content)
    elif phenomenon in ['advanced_cad', 'ADVANCED-CAD']:                               # nope
        return '' # (content)
    else: return None




if __name__ == '__main__':
    """
    argv[1] should be directory name with files? (for now)

    """
    main(sys.argv)
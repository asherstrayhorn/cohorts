import re
import nltk
from nltk.tokenize import word_tokenize


all_languages = [
	r'\bspanish\b',
	r'\bmandarin\b',
	r'\bcantonese\b',
	r'\bfrench\s+creole\b',
	r'\bhaitian\s+creole\b',       # technically, some of these are redundant
	r'\bcreole\b',                 # but it is nice to remember what we are looking for
	r'\bportuguese\b',
	r'\bcape\s+verdean\b',
	r'\bcape\s+verdean\s+creole\b',
	r'\bfrench\b',
	r'\bvietnamese\b',
	r'\bitalian\b',
	r'\bgerman\b',
	r'\bsomali\b',
	r'\byoruba\b',
	r'\bigbo\b',
	r'\bibo\b',
	r'\bkro\b',
	r'\bamharic\b',
	r'\barabic\b',
	r'\bhebrew\b',
	r'\bgreek\b',
	r'\bturkish\b',
	r'\balbanian\b',
	r'\barmenian\b',
	r'\bpersian\b',
	r'\burdu\b',
	r'\bhindi\b',
	r'\btelegu\b',
	r'\btamil\b',
	r'\bgujarathi\b',
	r'\bbengali\b',
	r'\bnepali\b',
	r'\bthai\b',
	r'\bkhmer\b',
	r'\bmon-khmer\b',
	r'\bmon\s+khmer\b',
	r'\blaotian\b',
    r'\btagalog\b',
	r'\bkorean\b',
	r'\bjapanese\b',
	r'\brussian\b',
	r'\bserbian\b',
	r'\bcroatian\b',
	r'\bserbo-croatian\b',
	r'\bhungarian\b',
	r'\bpolish\b',
	r'\bswedish\b',
	r'\bpatois\b',
    r'\binterpreter\b']



def eng(content):
    #sents = nltk.sent_tokenize(content)

    for language in all_languages:
        if re.search(language, content, re.I):   
                return 'not met'
    return 'met'
# drugs.py
import xml.etree.ElementTree as ET
import re
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer


NAME = ['marijuana', 'heroin', 'IVDU', 'lsd']

MOD_NAME = ['acid', 'speed', 'cocaine', 'oxycodone', 'methamphetamine', 'meth']

DRUG_WORD = ['drug', 'subtance']

NAME_MODS = ['abuse', 'drug', 'use', 'recreational', 'rec']

DRUG_MODS = ['illicit', 'illegal', 'psychedelic', 'recreational', 'rec', 'abuse']

#STATUS = ['occasional', 'ago', 'recent', 'former', 'past', 'previous', 'prior']

#HISTORY = ['history', 'h\/o']

NEGATION = [#'-',
            'NEGNEG',
            "no",
            "without",
            "n't",
            "not",
            "never",
            "none",
            "nor",
            "non",
            "denies",
            "negative"]
AFFIRMATION = ['+']

BARRIER_LEFT = [';']
BARRIER_RIGHT = [';', 'but']

LABEL_PUNCT = [':', '--']#, '-']  # regextok :  r'...|--?|...'

#STOP_LIST = ['of']

# Distances to look for feature in each direction
left_affirmation = 2
left_negation = 5
right_negation = 3
left_modifier = 2
right_modifier = 2
front_negation = 4


snowball_stemmer = SnowballStemmer("english")
stemmed_names = [snowball_stemmer.stem(word) for word in NAME]
stemmed_mod_names = [snowball_stemmer.stem(word) for word in MOD_NAME]
stemmed_drug_word = [snowball_stemmer.stem(word) for word in DRUG_WORD]
stemmed_name_mods = [snowball_stemmer.stem(word) for word in NAME_MODS]
stemmed_drug_mods = [snowball_stemmer.stem(word) for word in DRUG_MODS]
stemmed_negation = [snowball_stemmer.stem(word) for word in NEGATION]
#stemmed_history = [snowball_stemmer.stem(word) for word in HISTORY]

def gen_sents(sents):
    for seq in sents:
        for s in seq.split('\n\n'):
            yield s

def drug(contents):

    clean_text = re.sub('\\n', ' ', contents)
    clean_text = re.sub('\\t','', clean_text)
    clean_text = re.sub('[\s]{2,}', ' ', clean_text)

    sents = nltk.sent_tokenize(contents)
    #sents = gen_sents(sents)                # separate non period-terminated "sentences"

    for s in sents:

        s = s.replace('(-)', 'NEGNEG')
        s = s.replace('drug/', 'drug ')
        s = s.replace('/drug', ' drug')

        tokenizer = RegexpTokenizer(r'[a-zA-Z\']+|[;+:]|--|[0-9]+[-.]*[0-9]*')     # [;,]
        toks = tokenizer.tokenize(s)

        snowball_stemmer = SnowballStemmer("english")
        stemmed_tokens = [snowball_stemmer.stem(word.lower()) for word in toks]
        #print(stemmed_tokens)

        drug_score = 0
        abuse_score = 0
        token_count = len(stemmed_tokens)

        for j in range(token_count):
            # these names signal near definite abuse  |  increase score
            if stemmed_tokens[j] in stemmed_names:
                drug_score += 1
            
                # affirmation of near definite abuse indicators
                for i in range(1, left_affirmation + 1):
                    if j >= i and stemmed_tokens[j - i] in AFFIRMATION:
                        drug_score += 1
            
            # mod_names require a modifier to signal abuse   terms for certain drugs that have other uses
            #           once identified, look for those affirming modifiers before increasing score
            if stemmed_tokens[j] in stemmed_mod_names:
                if drug_score == 0:
                    for i in range(1, left_modifier+1):
                        if (j >= i) and (stemmed_tokens[j - i] in stemmed_name_mods):
                            drug_score += 1
                            break
                if drug_score == 0:
                    for i in range(1, right_modifier+1):
                        if (j < token_count - i) and (stemmed_tokens[j + i] in stemmed_name_mods):
                            drug_score += 1
                            break
            
            # drug_words also need modifiers.  These words occur frequently in non-abuse contexts
            if stemmed_tokens[j] in stemmed_drug_word:
                if drug_score == 0:
                    for i in range(1, left_modifier+1):
                        if (j >= i) and (stemmed_tokens[j - i] in stemmed_drug_mods):
                            drug_score += 1
                            break
                if drug_score == 0:
                    for i in range(1, right_modifier+1):
                        if (j < token_count - i) and (stemmed_tokens[j + i] in stemmed_drug_mods):
                            drug_score += 1
                            break            

            # unified negation

            # first look at the start of the sentence
            if drug_score > 0:
                tokens = stemmed_tokens
                #'''
                colon = -1
                for p in LABEL_PUNCT:
                    try:
                        colon = stemmed_tokens.index(p)
                        if colon in range(0, 6):  break
                        else:                     colon = -1        
                    except: pass

                if colon != -1 and colon < 6:
                    tokens = stemmed_tokens[colon+1:]
                for i in range(min(front_negation,token_count-colon-1)):
                    if tokens[i] in stemmed_negation:
                        drug_score -= 1
                        break

            # then, check in windows nearby
            if drug_score > 0:
                # Negation detection in left direciton                
                for i in range(1, left_negation+1):
                    if j >= i:
                        if stemmed_tokens[j - i] in BARRIER_LEFT:
                            break
                        if stemmed_tokens[j - i] in stemmed_negation:
                            drug_score -= 1
                            break

                # Negation detection in right direciton
                for i in range(1, right_negation+1):
                    if j < token_count - i:
                        if stemmed_tokens[j + i] in BARRIER_RIGHT:
                            break
                        if stemmed_tokens[j + i] in stemmed_negation:
                            drug_score -= 1
                            break
            #"""
            if drug_score > 0:
                return 'met'
            drug_score = 0
        

    return 'not met'
         





import re

OLDterms = ['agitation','dementia','Mental retardation','Alzheimer','AD dementia','ACH inhibitor','mental retardation','confusion','hallucinations']

terms = ['mental retardation', 'altered mental status', 'unable to recognize', 'pituitary adenoma', 'alzheimer']
# ACH inhibitor for Alzheimer
#my @terms = ('mental retardation', 'unable to recognize', 'pituitary adenoma', 'alzheimer') ; # ACH inhibitor for Alzheimer


# Family history should be removed FH: / FAMILY HISTORY:
# no / negation before

familyHistory = re.compile(r'(.*(fh:?)\b)|(.*(family history))')#, re.I)
negate        = re.compile(r'.*\b(no)\b')


def makes_decisions(text):
    result = 'met'
    for t in terms:
        re.sub(r' ', r'\\s+', t)
        cantDecideFlag = 0
        # search text for decision-relevant term.  Then look at context information to aid conclusion
        #for mt in re.finditer(t, text):
        mt = re.search(t, text, re.I)
        if mt:
            pretext = text[0:mt.span()[0]]  # take all chars before as context
            cantDecideFlag = 1
            mfh = familyHistory.search(pretext)         # see if family history heading is in pretext
            mn = negate.search(pretext)                 # seems too broad: "is there a no in pretext"
            if mfh:
                context = pretext[mfh.span()[1]:]    # context is everything after fh match
                cantDecideFlag = 0
                if re.search(r'history', context):    # context changed
                    cantDecideFlag = 1
                elif len(context) > 250:        # context too long
                    cantDecideFlag = 1
            elif mn:
                context = pretext[mn.span()[1]:]
                cantDecideFlag = 0
                if len(context) >= 10:          # context too long
                    cantDecideFlag = 1

        if cantDecideFlag == 1:
            result = 'not met'

    return result
    


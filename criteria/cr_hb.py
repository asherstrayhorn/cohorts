import re
import os

# for name in os.listdir("."):
#     if name.endswith(".xml"):
#         print(name)

filelist = [name for name in os.listdir(".") if name.endswith("-CH.xml")]


def hba1c(content):
    """
    input: string
    output: string as element with name="<value>"
    """
    A1C_CriteriaMet = False
    matchesA = re.findall(r"(?i)(A1c)([-=a-z\s.]*)(\d{1,2}[%.]\d*)", content)
    matchesA += re.findall(r"(?i)(A1c)(\s*\d{1,2}\/\d{1,2}\/\d{2,4}\s*)(\d{1,2}\.\d+)", content)
    for match in matchesA:
        value = match[2]
        value = re.sub(r"%$","",value)
        value = float(value)
        if value >= 6.5:
            if value <= 9.5:
                A1C_CriteriaMet = True
        else:
            continue

    #print(file,A1C_CriteriaMet, matchesA)
    if A1C_CriteriaMet is True:
        return 'met'
    else:
        return 'not met'



def creatinine(content):
    """
    same deal as hba1c
    """
    Cr_CriteriaMet = False
    matchesC = re.findall(r"(?i)\b(creatinine|creat|cre|cr)\b([-a-z.\s()]+)(\d{1,2}\.\d+)(\s*([H*]|\([H*]\)))?", content)
    matchesC += re.findall(r"(?i)\b(creatinine|creat|cre|cr)\b(\s+\d{1,2}\/\d{1,2}\/\d{2,4}\s+)(\d{1,2}\.\d+)", content)

    for match in matchesC:
        #print(match)
        if match[1].find("take") != -1:
            continue
        if len(match) > 3 and match[3] != "" :
            #print('#'+match[3]+'#')
            Cr_CriteriaMet = True
            continue
        value = float(match[2])
        if value > 1.5:
            if value <= 10.0:
                Cr_CriteriaMet = True
        else:
            continue
    #print(file,Cr_CriteriaMet)

    if Cr_CriteriaMet is True:
        return 'met'
    else:
        return 'not met'

    # preprocess to clean character (endash)
    # content = re.sub(r"&#8211;","--", content)

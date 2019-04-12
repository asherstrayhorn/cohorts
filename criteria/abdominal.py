import nltk
import re
import pandas as pd
def perf_measure(y_actual, y_hat):
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(len(y_hat)):
        if y_actual[i]==y_hat[i]=='met':
           TP += 1
        if y_hat[i]=='not met' and y_actual[i]!=y_hat[i]:
           FP += 1
        if y_actual[i]==y_hat[i]=='not met':
           TN += 1
        if y_hat[i]=='met' and y_actual[i]!=y_hat[i]:
           FN += 1

    return (TP, FP, TN, FN)
pattern1=re.compile('Past History:?\s*[\w+.,;#&\/\-\=\%\(\)""\s]*|[P|p]ast [M|m]edical [H|h]istory:?\s*[\w+.,;#&""\/\-\=\%\(\)\s]*|PAST MEDICAL HISTORY:?\s*[\w+.;,#&"\/\-\=\%\(\)\s]*|PMHx?/PSHx?:?\s*[\s\w+.,;#&"\/\-\=\%\(\)\s]*|PMHx:?\s+[\s\w+.,;#&"\/\-\=\%\(\)\s]*|PMH:?\s*[\s\w+.,;#&"\/\-\=\%\(\)\s]*')
pattern2=re.compile('Surgeries:?\s*[\w+.,;#&\/\-\=\%\(\)""\s]*|Surgery:?\s*[\w+.,;#&\/\-\=\%\(\)""\s]*|Past [S|s]urgical [H|h]istory:?\s*[\w+.,;#&""\/\-\=\%\(\)\s]*|PAST SURGICAL HISTORY:\s*[\w+.,;#&""\/\-\=\%\(\)\s]*|PSHx:?\s*[\w+.,;#&"\/\-\=\%\(\)\s]*|PSH:?\s*[\w+.,;#&"\/\-\=\%\(\)\s]*|P[S|s]urHx:?\s*[\w+.,;#&"\/\-\=\%\(\)\s]*|P[S|s]urHx:?\s*[\w+.,;#&"\/\-\=\%\(\)\s]*')
pattern3=re.compile('Prior surgery includes:?\s*[\w+.,;#&\'\/\-\=\%\(\)""\s]*|Hx:?\s*[\w+.,#&;\'\+\/\-\=\%\(\)""\s]*|[P|p]ast [M|m]edical history includes:?\s*[\w+.,;#&\'\/\-\=\%\(\)""\s]*|FINAL DIAGNOSIS:?\s*[\w+.,;#&\'\/\-\=\%\(\)""\s]*')
pattern4=re.compile('History of Present Illness:?\s*[\w+.,;#&\'\/\-\=\%\(\)""\s]*|HPI:?\s*[\w+.,;#&\'\/\-\=\%\(\)""\s]*')
pattern5=re.compile('PROCEDURE:?\s*[\w+.,;#&\'\/\-\=\%\(\)""\s]*|[P|p]rocedure:?\s*[\w+.,;#&\'\/\-\=\%\(\)""\s]*')
bigr = []
trig=[]
met = []
final=0

surgery_list=['bowel surgery','kidney tx','tah','aaa repair','colostomy','cholecystectomy','colectomy','colonoscopic polypectomy','roux-en-y','appendectomy','colonic polyps removed','tah-bso','total abdominal hysterectomy with bilateral salpingooophorectomy','bowel obstruction','umbilical hernia repair','small bowel obstruction','large bowel obstruction',
              'gastrectomy','esophagojejunostomy','pancreatectomy','splenectomy','kidney transplant','renal transplant','llrtx','tah/bso','triple-a repair','papillotomy','colon cancer resection','gastric bypass','hysterectomy','small intestine resection','large intestine resection','cytoreductive','liver transplant','colon resection','liver tx','myomectomy',
              'oophorectomy','radical prostatectomy','bilateral tubal ligation','polypectomy','bilateral tubal ligation','aortic aneurysm repair','whipple','pancreaticoduodenectomy','salpingo-oophorectomy','ileocecotomy','esophagectomy','bso','nephrectomy','small-bowel obstruction','chole','appy','lithotripsy','lap chole', 'laparoscopic', 'laparascopy','appy']
positive=['s/p','underwent','performed','had','post','history','h/o','has','another','-s/p',':','after']
headlist=['history','examination','diagnosis','illness','plan','medication','allergies','systems','data','studies','a/p','problems','sh','hpi','pmh','admission','famhx',
          'sochx','psh','ros','pe','labs','assessment','addendum','signs','impression','hx','meds','pexam','recs','evaluation',
          'complaint','diagnoses','procedures','procedure','pmh/psh','home','testing','recommendation']
# 'lap chole', 'laparoscopic', 'laparascopy','appy',''lithotripsy'


def mat(text, count,rec,span=[]):
    n=0
    y=0

    cleared_data=list()
    for i in text:
        new=rec
        y=y+1
        i = i.lower()

        words = nltk.word_tokenize(i)
        n=y
        d=0


        for z in words:
            re.sub('[,\.]', ' ', z)
            cleared_data.append(z)


        for j in words:
            if j in surgery_list:
                count = count + 1

        bigr = list(nltk.bigrams(cleared_data))
        # print(bigr)
        for b in bigr:


            if b[0] + ' ' + b[1] in surgery_list:
                count = count + 1
                break
        if count == 0:
            trig = list(nltk.trigrams(cleared_data))
            # print(trig)
            for k in trig:

                if k[0] + ' ' + k[1] + ' ' + k[2] in surgery_list:
                    count = count + 1
                    break

    return count

def abd(rec):
    try:
        count=0
        a=list()
        text=(re.findall(pattern1,rec))
        for m in pattern1.finditer(rec):
            a.append(m.end())

        # print(a)
        count=mat(text,count,rec,a)
        a = list()
        second = (re.findall(pattern2, rec))
        for m in pattern2.finditer(rec):
            a.append(m.end())
        # print(second)
        summ=mat(second,count,rec,a)
        if summ==0:
            a = list()
            third = (re.findall(pattern3, rec))
            for m in pattern3.finditer(rec):
                a.append(m.end())
            # print(third)
            summ=mat(third,summ,rec,a)

        if summ==0:
            fifth = (re.findall(pattern5, rec))
            # print(third)
            summ=mat(fifth,summ,rec,a)
        if summ==0:
            cleared_data=list()
            word=nltk.word_tokenize(rec.lower())
            for z in word:
                re.sub('\,\.', ' ', z)
                cleared_data.append(z)
            for j in range(0,len(cleared_data)):
                if cleared_data[j].lower() in surgery_list:
                    if cleared_data[j - 1] in positive or cleared_data[j - 2] in positive:
                        summ = summ + 1
                    elif cleared_data[j + 1] in positive or cleared_data[j + 2] in positive:
                        summ = summ + 1
            if summ==0:
                # bigr = list(nltk.bigrams(rec.split()))
                # print(bigr)
                for b in range(0,len(cleared_data)-1):

                    if cleared_data[b].lower() + ' ' + cleared_data[b+1].lower() in surgery_list:
                        if cleared_data[b - 1].lower() in positive or cleared_data[b-2].lower() in positive:
                            summ = summ + 1
                        elif cleared_data[b+2].lower() in positive or cleared_data[b+ 3].lower() in positive:
                            summ = summ + 1
                        break

            if summ==0:
                # bigr = list(nltk.bigrams(rec.split()))
                # print(bigr)
                for b in range(0,len(cleared_data)-2):

                    if cleared_data[b].lower() + ' ' + cleared_data[b+1].lower()+' '+cleared_data[b+2].lower() in surgery_list:
                        if cleared_data[b - 1].lower() in positive or cleared_data[b-2].lower() in positive:
                            summ = summ + 1
                        elif cleared_data[b+3].lower() in positive or cleared_data[b+ 4].lower() in positive:
                            summ = summ + 1
                        break

        if summ==0:
            return 'not met'
            met.append('not met')
        else:
            # print(str(i)+'.xml')
            return 'met'
            met.append('met')

    except Exception as e :
        print(str(e))
        return 'ERR'


        # print(met)
def metrics():
    df=pd.read_csv('labels.csv')     # eave this stuff around for ideas for measuring performance later
    check=list(df['ABDOMINAL'])
    # print(len(check),len(met))
    for i in range(0,len(met)):
        if met[i]==check[i]:

            final=final+1
        # else:
            # print(i)
    # print(len(met))
    prop=final/len(met)
    print(str(prop))

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=PendingDeprecationWarning)
        import nltk
        
        from sklearn.metrics import precision_score, \
            recall_score, confusion_matrix, classification_report, \
            accuracy_score, f1_score
    print ('Accuracy:', accuracy_score(met, check))
    # print( 'F1 score:', f1_score(met, check))
    v=perf_measure(met,check)
    print(v)
    recall=v[0]/(v[0]+v[3])
    precision=v[0]/(v[0]+v[1])
    f1=(2*(precision*recall))/(precision+recall)
    print(recall,precision,f1)
    print(len(surgery_list))


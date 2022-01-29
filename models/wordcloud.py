from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import multidict as multidict
from collections import Counter
import json
import datetime
import os
plt.switch_backend('agg')
def removePunctuation(text):
    text = re.sub(r'[{}]+'.format('!,;:?`"\'、，；'),' ',text)
    return text.strip()

def getFrequencyDictForText0(sentence,pro):
    global tmpDict0
    # making dict for counting frequencies
    sentence=removePunctuation(sentence)
    for text in sentence.split(" "):
        if len(text)<3 or re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text) or (re.match("^[A-Za-z]+$", text) is None):
            continue
        val = tmpDict0.get(text, [0,[]])
        pros=val[1]
        if pro not in pros:
            pros.append(pro)
        tmpDict0[text.lower()] = [val[0] + 1,pros]

def getFrequencyDictForText1(sentence,pro):
    global tmpDict1
    # making dict for counting frequencies
    sentence=removePunctuation(sentence)
    for text in sentence.split(" "):
        if len(text)<3 or re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text) or (re.match("^[A-Za-z]+$", text) is None):
            continue
        val = tmpDict1.get(text, [0,[]])
        pros=val[1]
        if pro not in pros:
            pros.append(pro)
        tmpDict1[text.lower()] = [val[0] + 1,pros]
    
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj,datetime.timedelta):
            return obj.seconds
        else:
            return json.JSONEncoder.default(self,obj)

def drawwordcloud():
    global tmpDict0,tmpDict1
    finalbody0=''
    finalbody1=''
    current_work_dir = os.path.dirname(__file__) 
    with open(current_work_dir+'/../data/issuedata.json') as f:
        issuestr = json.load(f)
    issuedic = json.loads(issuestr)
    issuedata = issuedic['issuedata']
    lst=[]
    for i in range(len(issuedata)):
        lst.append(issuedata[i][0])
    finaldata=pd.DataFrame(lst)
    finaldata=finaldata.values.tolist()
    

    finalbody0=[]
    finalbody1=[]
    for d in finaldata:
        pro=d[1]
        body=d[39]
        p=re.compile(r"```.+?```",flags=re.S)
        s=p.sub("",body)
        body=" ".join(s.split())
        p=re.compile(r"http[:/\w\.]+")
        s=p.sub("",body)
        body=" ".join(s.split())
        body.lower()
        if d[37]==0:#clscmt
            finalbody0.append([body,pro])
        else:
            finalbody1.append([body,pro])
    tmpDict0 = {}
    tmpDict1 = {}

    for i in finalbody0:
        getFrequencyDictForText0(i[0],i[1])

    for i in finalbody1:
        getFrequencyDictForText1(i[0],i[1])

    for key in list(tmpDict0.keys()):
        val0 = tmpDict0.get(key, [0,[]])
        val1 = tmpDict1.get(key, [0,[]])
        if len(list(set(val0[1]+val1[1])))<5:
            del tmpDict0[key]

    for key in list(tmpDict1.keys()):
        val0 = tmpDict0.get(key, [0,[]])
        val1 = tmpDict1.get(key, [0,[]])
        if len(list(set(val0[1]+val1[1])))<5:
            del tmpDict1[key]

    fullTermsDict0 = multidict.MultiDict()
    for key in tmpDict0:
        val0 = tmpDict0.get(key, [0,[]])
        val1 = tmpDict1.get(key, [0,[]])
        fullTermsDict0.add(key, pow(val0[0], 2)/(val0[0]+val1[0]))
    
    fullTermsDict1 = multidict.MultiDict()
    for key in tmpDict1:
        val0 = tmpDict0.get(key, [0,[]])
        val1 = tmpDict1.get(key, [0,[]])
        fullTermsDict1.add(key, pow(val1[0], 2)/(val0[0]+val1[0]))


    wc = WordCloud(
    background_color='white',
    width=500,
    height=350,
    max_font_size=100,
    min_font_size=3,
    max_words=50,
    relative_scaling=0.5,
    collocations=False,
    min_word_length=3,
    #stopwords=stopwords,
    mode='RGBA'
        #colormap='pink'
    )
    wc.generate_from_frequencies(fullTermsDict0)
    wc.to_file(r"wordcloud0.png")
    wc.generate_from_frequencies(fullTermsDict1)
    wc.to_file(r"wordcloud1.png")



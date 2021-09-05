import pandas as pd
import re
import textstat
import numpy as np
def count_code_number(str):
    p=re.compile(r"```.+?```",flags=re.S)
    return len(p.findall(str))

def delete_code(str):
    p=re.compile(r"```.+?```",flags=re.S)
    s=p.sub("",str)
    return " ".join(s.split())

def count_url(str):
    def notPic(s):
        if s.endswith("jpg") or s.endswith("jpeg") or s.endswith("png"):
            return False
        return True
    p=re.compile(r"http[:/\w\.]+")
    lst=list(filter(notPic,p.findall(str)))

    return len(lst)

def count_pic(str):
    p=re.compile(r"http[:/\w\.]+")
    def isPic(s):
        if s.endswith("jpg") or s.endswith("jpeg") or s.endswith("png"):
            return True
        return False
    lst=list(filter(isPic,p.findall(str)))
    return len(lst)

def delete_url(str):
    p=re.compile(r"http[:/\w\.]+")
    s=p.sub("",str)
    return " ".join(s.split())

def change_language_to_index(str):
    lst=['JavaScript', 'HTML', 'TypeScript', 'Python', 'PHP', 'C#', 'Java', 'C', 'C++']
    res=[0,0,0,0,0,0,0,0,0]
    res[lst.index(str)]=1
    return res
    
def count_text_len(str):
    return len(str.split())


def get_label(clscmt):
    if clscmt<threshold:
        return 1
    return 0

def Normalization(df,str):
    mean=df[str].mean()
    std=df[str].std()
    def norm(x):
        return (x-mean)/std
    x=df[str].apply(norm)

    return x


def count_positive_words(str):
    lst=['enabled', 'vs', 'open', 'actual', 'setting', 'first', 'json', 'form', 'editor', 'default', 'show', 'node', 'vscode', 'comic']
    count=0
    str=str.lower()
    lst_word=str.split()
    for i in lst_word:
        if i in lst:
            count+=1

    return count

def count_negative_words(str):
    lst=['possible', 'function', 'blob', 'link', 'learn', 'report', 'installed', 'commit', 'case', 'feature', 'oa', 'doc', 'object', 'create']
    count=0
    str=str.lower()
    lst_word=str.split()
    for i in lst_word:
        if i in lst:
            count+=1

    return count

def generateRate(lst):
    c1=0
    c2=0
    for i in lst:
        if i!= None:
            c1+=1
            if i<threshold:
                c2+=1

    if c1==0:
        return 0
    else:
        return c2/c1
        
def generateNum(lst):
    c1=0    
    for i in lst:
        if i!= None:
            if i<threshold:
                c1+=1
    return c1

def ifrptnew(rptcmt):
    if rptcmt<threshold:
        return 1
    return 0


def getratio(lst):
    if lst is None:
        return 0
    else:
        lst=[d for d in lst if d is not None]
        if lst==[]:
            return 0
        pnum=sum(d<threshold for d in lst)
        nnum=len(lst)-pnum
        if pnum==0:
            pnum=0.1
        return nnum/pnum

def getissnum(lst):
    if lst is None:
        return 0
    else:
        return len(lst)
if __name__=="__main__":
    Threshold=[1,2,3,4,5]
    data=np.load('data.npy',allow_pickle=True)
    data=data.tolist()
    lst=[]
    for i in range(len(data)):
        lst.append(data[i][0])
  
    for threshold in Threshold:
        df=pd.DataFrame(lst)
        df["NumOfCode"]=df["body"].apply(count_code_number)
        df["body"]=df["body"].apply(delete_code)
        df["NumOfUrls"]=df["body"].apply(count_url)
        df['NumOfPics']=df["body"].apply(count_pic)
        df["body"]=df["body"].apply(delete_url)
        df['coleman_liau_index']=df['body'].apply(textstat.coleman_liau_index)
        df['flesch_reading_ease']=df['body'].apply(textstat.flesch_reading_ease)
        df['flesch_kincaid_grade']=df['body'].apply(textstat.flesch_kincaid_grade)
        df['automated_readability_index']=df['body'].apply(textstat.automated_readability_index)
        
        df['PositiveWords']=df['body'].apply(count_positive_words)
        df['NegativeWords']=df['body'].apply(count_negative_words)

        df["LengthOfTitle"]=df["title"].apply(count_text_len)
        df["LengthOfDescription"]=df["body"].apply(count_text_len)

        df['proissnewratio']=df['isslist'].apply(generateRate)

        df["ownerissnewratio"]=df["ownerissues"].apply(generateRate)
        df['proissnewnum']=df['isslist'].apply(generateNum)

        df["ownerissnewnum"]=df["ownerissues"].apply(generateNum)
        df['labelcategory']=df['labels']
        df['labels']=df["clscmt"].apply(get_label)


        df["rptisnew"]=df["rptcmt"].apply(ifrptnew)

        df["rptnpratio"]=df["rptisscmtlist"].apply(getratio)
        df["rptissnum"]=df["rptisscmtlist"].apply(getissnum)     

        df.to_pickle("dataset1_threshold_"+str(threshold)+".pkl")

        
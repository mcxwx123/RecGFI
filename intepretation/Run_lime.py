import pandas as pd
import numpy as np
import lime
import lime.lime_tabular
import data_utils_lime
import scipy.io
import csv
import sys
sys.path.append('../')
from models.utils import vectorize
import time
from xgboost import XGBClassifier

def process_data(df):
    
    #Probability of predictions
    df1=df[df['labels']==1]
    df0=df[df['labels']==0]
    list0=df0['scores'].values.tolist()
    list1=df1['scores'].values.tolist()
    scipy.io.savemat('data/predata.mat',{'list0':list0, 'list1':list1})
    
    proidlist=df['proid'].values.tolist()
    proid=max(proidlist,key=proidlist.count)
    
    for i in range(df.shape[0]):
        if df["proid"].iloc[i]==proid:
            for t in range(len(namelist)):
                oneitem=df["lime_lst"].iloc[i][t]
                for m in range(len(namelist)):
                    if namelist[m] in oneitem[0]:
                        if ("event_ex10" in oneitem[0] and "event_ex10" not in namelist[m]) or ("openissratio" in oneitem[0] and "openissratio" not in namelist[m]) or ("labelevent" in oneitem[0] and "labelevent" not in namelist[m]) or ("ownerpronum" in oneitem[0] and "ownerpronum" not in namelist[m]) or ("ownerissnewratio" in oneitem[0] and "ownerissnewratio" not in namelist[m]) or ("ownerissnewnum" in oneitem[0] and "ownerissnewnum" not in namelist[m]) or ("rptpronum" in oneitem[0] and "rptpronum" not in namelist[m]) or ("lc10" in oneitem[0] and "lc10" not in namelist[m]) or ("lc11" in oneitem[0] and "lc11" not in namelist[m]) or ("lc12" in oneitem[0] and "lc12" not in namelist[m]) or ("le10" in oneitem[0] and "le10" not in namelist[m]) or ("le11" in oneitem[0] and "le11" not in namelist[m]) or ("le12" in oneitem[0] and "le12" not in namelist[m]) or ("event10" in oneitem[0] and "event10" not in namelist[m]) or ("event11" in oneitem[0] and "event11" not in namelist[m]) or ("event12" in oneitem[0] and "event12" not in namelist[m]) or ("event13" in oneitem[0] and "event13" not in namelist[m]) or ("event14" in oneitem[0] and "event14" not in namelist[m]) or ("event15" in oneitem[0] and "event15" not in namelist[m]) or ("event16" in oneitem[0] and "event16" not in namelist[m]) or ("event17" in oneitem[0] and "event17" not in namelist[m]) or ("event18" in oneitem[0] and "event18" not in namelist[m]) or ("event19" in oneitem[0] and "event19" not in namelist[m]) or ("event20" in oneitem[0] and "event20" not in namelist[m]) or ("event21" in oneitem[0] and "event21" not in namelist[m]) or ("event22" in oneitem[0] and "event22" not in namelist[m]) or ("event23" in oneitem[0] and "event23" not in namelist[m]) or ("event24" in oneitem[0] and "event24" not in namelist[m]) or ("event25" in oneitem[0] and "event25" not in namelist[m]) or ("event26" in oneitem[0] and "event26" not in namelist[m]) or ("event27" in oneitem[0] and "event27" not in namelist[m]) or ("event28" in oneitem[0] and "event28" not in namelist[m]) or ("event29" in oneitem[0] and "event29" not in namelist[m]) or ("event30" in oneitem[0] and "event30" not in namelist[m]) or ("event31" in oneitem[0] and "event31" not in namelist[m]) or ("event32" in oneitem[0] and "event32" not in namelist[m]) or ("event33" in oneitem[0] and "event33" not in namelist[m]) or ("event34" in oneitem[0] and "event34" not in namelist[m]) or ("event35" in oneitem[0] and "event35" not in namelist[m]) or ("event36" in oneitem[0] and "event36" not in namelist[m]) or ("event37" in oneitem[0] and "event37" not in namelist[m]) or ("event38" in oneitem[0] and "event38" not in namelist[m]):
                            continue
                        else:
                            lists1[m].append(oneitem[1])
    scipy.io.savemat('data/oneproft.mat',{'onelist':lists1})
    
    for i in range(df.shape[0]):
        proid=df["proid"].iloc[i]
        if proid not in proidlists:
            proidlists.append(proid)
        ind=proidlists.index(proid)
        for t in range(len(namelist)):
            oneitem=df["lime_lst"].iloc[i][t]
            for m in range(len(namelist)):
                if namelist[m] in oneitem[0]:
                    if ("event_ex10" in oneitem[0] and "event_ex10" not in namelist[m]) or ("openissratio" in oneitem[0] and "openissratio" not in namelist[m]) or ("labelevent" in oneitem[0] and "labelevent" not in namelist[m]) or ("ownerpronum" in oneitem[0] and "ownerpronum" not in namelist[m]) or ("ownerissnewratio" in oneitem[0] and "ownerissnewratio" not in namelist[m]) or ("ownerissnewnum" in oneitem[0] and "ownerissnewnum" not in namelist[m]) or ("rptpronum" in oneitem[0] and "rptpronum" not in namelist[m]) or ("lc10" in oneitem[0] and "lc10" not in namelist[m]) or ("lc11" in oneitem[0] and "lc11" not in namelist[m]) or ("lc12" in oneitem[0] and "lc12" not in namelist[m]) or ("le10" in oneitem[0] and "le10" not in namelist[m]) or ("le11" in oneitem[0] and "le11" not in namelist[m]) or ("le12" in oneitem[0] and "le12" not in namelist[m]) or ("event10" in oneitem[0] and "event10" not in namelist[m]) or ("event11" in oneitem[0] and "event11" not in namelist[m]) or ("event12" in oneitem[0] and "event12" not in namelist[m]) or ("event13" in oneitem[0] and "event13" not in namelist[m]) or ("event14" in oneitem[0] and "event14" not in namelist[m]) or ("event15" in oneitem[0] and "event15" not in namelist[m]) or ("event16" in oneitem[0] and "event16" not in namelist[m]) or ("event17" in oneitem[0] and "event17" not in namelist[m]) or ("event18" in oneitem[0] and "event18" not in namelist[m]) or ("event19" in oneitem[0] and "event19" not in namelist[m]) or ("event20" in oneitem[0] and "event20" not in namelist[m]) or ("event21" in oneitem[0] and "event21" not in namelist[m]) or ("event22" in oneitem[0] and "event22" not in namelist[m]) or ("event23" in oneitem[0] and "event23" not in namelist[m]) or ("event24" in oneitem[0] and "event24" not in namelist[m]) or ("event25" in oneitem[0] and "event25" not in namelist[m]) or ("event26" in oneitem[0] and "event26" not in namelist[m]) or ("event27" in oneitem[0] and "event27" not in namelist[m]) or ("event28" in oneitem[0] and "event28" not in namelist[m]) or ("event29" in oneitem[0] and "event29" not in namelist[m]) or ("event30" in oneitem[0] and "event30" not in namelist[m]) or ("event31" in oneitem[0] and "event31" not in namelist[m]) or ("event32" in oneitem[0] and "event32" not in namelist[m]) or ("event33" in oneitem[0] and "event33" not in namelist[m]) or ("event34" in oneitem[0] and "event34" not in namelist[m]) or ("event35" in oneitem[0] and "event35" not in namelist[m]) or ("event36" in oneitem[0] and "event36" not in namelist[m]) or ("event37" in oneitem[0] and "event37" not in namelist[m]) or ("event38" in oneitem[0] and "event38" not in namelist[m]):
                       continue
                    else:
                        lists2[ind][m].append(oneitem[1])
    for i in range(len(lists2)):
        for m in range(len(namelist)):
            if lists2[i][m]==[]:
                lists2[i][m]=0
            else:
                if np.mean(lists2[i][m])>0:
                    lists2[i][m]=1
                else:
                    lists2[i][m]=0
    scipy.io.savemat('data/allproft.mat',{'alllist':lists2})

    cmt1=200
    cmt2=400
    cmt3=600
    with open ('/data/test.csv','r') as f:
        valuedf=pd.read_csv(f)
    for i in range(df.shape[0]):
        rptcmt=valuedf['rptcmt'].iloc[i]
        if rptcmt<cmt1:
            ind=0
        else:
            if rptcmt<cmt2:
                ind=1
            else:
                if rptcmt<cmt3:
                    ind=2
                else:
                    ind=3
        for t in range(len(namelist)):
            oneitem=df["lime_lst"].iloc[i][t]
            for m in range(len(namelist)):
                if namelist[m] in oneitem[0]:
                    if ("event_ex10" in oneitem[0] and "event_ex10" not in namelist[m]) or ("openissratio" in oneitem[0] and "openissratio" not in namelist[m]) or ("labelevent" in oneitem[0] and "labelevent" not in namelist[m]) or ("ownerpronum" in oneitem[0] and "ownerpronum" not in namelist[m]) or ("ownerissnewratio" in oneitem[0] and "ownerissnewratio" not in namelist[m]) or ("ownerissnewnum" in oneitem[0] and "ownerissnewnum" not in namelist[m]) or ("rptpronum" in oneitem[0] and "rptpronum" not in namelist[m]) or ("lc10" in oneitem[0] and "lc10" not in namelist[m]) or ("lc11" in oneitem[0] and "lc11" not in namelist[m]) or ("lc12" in oneitem[0] and "lc12" not in namelist[m]) or ("le10" in oneitem[0] and "le10" not in namelist[m]) or ("le11" in oneitem[0] and "le11" not in namelist[m]) or ("le12" in oneitem[0] and "le12" not in namelist[m]) or ("event10" in oneitem[0] and "event10" not in namelist[m]) or ("event11" in oneitem[0] and "event11" not in namelist[m]) or ("event12" in oneitem[0] and "event12" not in namelist[m]) or ("event13" in oneitem[0] and "event13" not in namelist[m]) or ("event14" in oneitem[0] and "event14" not in namelist[m]) or ("event15" in oneitem[0] and "event15" not in namelist[m]) or ("event16" in oneitem[0] and "event16" not in namelist[m]) or ("event17" in oneitem[0] and "event17" not in namelist[m]) or ("event18" in oneitem[0] and "event18" not in namelist[m]) or ("event19" in oneitem[0] and "event19" not in namelist[m]) or ("event20" in oneitem[0] and "event20" not in namelist[m]) or ("event21" in oneitem[0] and "event21" not in namelist[m]) or ("event22" in oneitem[0] and "event22" not in namelist[m]) or ("event23" in oneitem[0] and "event23" not in namelist[m]) or ("event24" in oneitem[0] and "event24" not in namelist[m]) or ("event25" in oneitem[0] and "event25" not in namelist[m]) or ("event26" in oneitem[0] and "event26" not in namelist[m]) or ("event27" in oneitem[0] and "event27" not in namelist[m]) or ("event28" in oneitem[0] and "event28" not in namelist[m]) or ("event29" in oneitem[0] and "event29" not in namelist[m]) or ("event30" in oneitem[0] and "event30" not in namelist[m]) or ("event31" in oneitem[0] and "event31" not in namelist[m]) or ("event32" in oneitem[0] and "event32" not in namelist[m]) or ("event33" in oneitem[0] and "event33" not in namelist[m]) or ("event34" in oneitem[0] and "event34" not in namelist[m]) or ("event35" in oneitem[0] and "event35" not in namelist[m]) or ("event36" in oneitem[0] and "event36" not in namelist[m]) or ("event37" in oneitem[0] and "event37" not in namelist[m]) or ("event38" in oneitem[0] and "event38" not in namelist[m]):
                        continue
                    else:
                        lists3[ind][m].append(oneitem[1])

    scipy.io.savemat('data/ftvalue.mat',{'valuelist':lists3})
    
    

    for i in range(df.shape[0]):
        rptcmt=valuedf['rptcmt'].iloc[i]
        if rptcmt<cmt1:
            ind=0
        else:
            if rptcmt<cmt2:
                ind=1
            else:
                if rptcmt<cmt3:
                    ind=2
                else:
                    ind=3
        if df['labels'].iloc[i]==0:
            lists4[ind].append(df['scores'].iloc[i])
        else:
            lists5[ind].append(df['scores'].iloc[i])
    scipy.io.savemat('data/rptpre.mat',{'rptprelist0':lists4,'rptprelist1':lists5})

if __name__=="__main__":
    c=[]
    for i in range(50):
        c.append("title"+str(i))
    for i in range(50):
        c.append("description"+str(i))
    for i in range(50):
        c.append("com"+str(i))
    X_train, X_test, y_train, y_test, proid_test= data_utils_lime.load_train_test_data("../data/dataset2_threshold_1.pkl",vectorize.Vectorizer('TFIDF', ngram_range=(1, 1)),2,9)

    model = XGBClassifier()

    model.fit(X_train,y_train)
    for key in c:
        del X_train[key]

    text=X_test[c]
    for key in c:
        del X_test[key]


    explainer = lime.lime_tabular.LimeTabularExplainer(training_data=X_train.values,mode="regression",feature_names=X_train.columns,verbose=True)
    score=[]
    lime_lst=[]   
    for i in range(len(X_test)):
        def p(data):
            data=pd.DataFrame(data)
            data.columns=X_train.columns
        
            x=[text.iloc[i:i+1,:] for z in range(data.shape[0])]
            t=pd.concat(x,axis=0)
            t.reset_index(drop=True, inplace=True)
            data.reset_index(drop=True, inplace=True)

            d=pd.concat([t,data],axis=1)
        
        
            return model.predict_proba(d)[:,1]
        time1=time.time()
    
    

        exp = explainer.explain_instance(data_row=X_test.iloc[i],num_features=106, predict_fn=p)


        score.append(np.array(exp.predicted_value))
        lime_lst.append(exp.as_list())

    X_test["labels"]=y_test["labels"].values
    X_test["proid"]=proid_test["proid"].values
    X_test["scores"]=score
    X_test["lime_lst"]=lime_lst

    df=X_test[["proid","scores","labels","lime_lst"]]

    namelist=["LengthOfTitle","LengthOfDescription","NumOfUrls","NumOfPics","NumOfCode", "PositiveWords","NegativeWords","coleman_liau_index","automated_readability_index", "flesch_reading_ease", "flesch_kincaid_grade", "commentnum","ownerallpr","ownerpr","ownercmt","ownerallcmt","ownerpronum","ownerstar","ownerfoll","owneralliss","owneriss","ownerissnewratio","ownerissnewnum", #23
    "proissnewratio","proissnewnum","openiss","clsisst","pro_star","procmt","contributornum","proclspr","rptallpr","rptpr","rptcmt","rptallcmt","rptpronum","rptstar","rptfoll","rptalliss",'rpthascomment', 'rptisnew', 'rpthasevent',"rptnpratio","rptissnum",#44
    "lc0","lc1","lc2","lc3","lc4","lc5","lc6","lc7","lc8","lc9","lc10","lc11","lc12",#57
    "le0","le1","le2","le3","le4","le5","le6","le7","le8","le9","le10","le11","le12",#70
    "event_ex0","event_ex1","event_ex2","event_ex3","event_ex4","event_ex5","event_ex6","event_ex7","event_ex8","event_ex9","event_ex10","event0","event1","event2","event3","event4","event5","event6","event7","event8","event9","event10","event11","event12","event13","event14","event15","event16","event17","event18","event19","event20","event21","event22","event23","event24"]#106

    lists1 = [[] for _ in range(len(namelist))]
    lists2=[[[] for _ in range(len(namelist))] for _ in range(100)]
    lists3=[[[] for _ in range(len(namelist))] for _ in range(4)]
    lists4=[[] for _ in range(4)]
    lists5=[[] for _ in range(4)]
    lists6 = [[] for _ in range(len(namelist))]

    proidlists=[]

    process_data(df)


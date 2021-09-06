import pandas as pd
import numpy as np
import lime
from utils import data_utils_lime
from utils import vectorize
import time


from xgboost import XGBClassifier
c=[]
for i in range(50):
    c.append("title"+str(i))
for i in range(50):
    c.append("description"+str(i))
for i in range(50):
    c.append("com"+str(i))
X_train, X_test, y_train, y_test, proid_test= data_utils_lime.load_train_test_data("/data/dataset2_threshold_1.pkl",vectorize.Vectorizer('TFIDF', ngram_range=(1, 1)),2,9)

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
    
    print(time.time()-time1)

X_test["labels"]=y_test["labels"].values
X_test["proid"]=proid_test["proid"].values
X_test["scores"]=score
X_test["lime_lst"]=lime_lst

res=X_test[["proid","scores","labels","lime_lst"]]
res.to_pickle("lime_res.pkl")
print(res)
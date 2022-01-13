from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from models.utils import metrics_util
from models.utils import data_utils
from models.utils import data_utils_ablate_comment
from models.utils import data_utils_ablate_event
from models.utils import data_utils_ablate_experience
from models.utils import data_utils_ablate_label
from models.utils import data_utils_ablate_rpt
from models.utils import data_utils_ablate_issue
from models.utils import data_utils_ablate_project
from models.utils import data_utils_baseline_comment
from models.utils import data_utils_baseline_experience
from models.utils import data_utils_baseline_issue
from models.utils import data_utils_baseline_rpt
from models.utils import data_utils_baseline_project
from models.utils import data_utils_baseline_label
from models.utils import data_utils_baseline_event
from models.utils import vectorize
import os

def write_result(file, str):
    f = open(file, "a+")
    f.write(str+"\n")
    f.close()

class XGB:
    def __init__(self, vectorizer, dataset_index,threshold,m,fold):
        self.data = "../data/dataset"+str(dataset_index)+"_threshold_"+str(threshold)+".pkl"
        current_work_dir = os.path.dirname(__file__) 
        self.data = os.path.join(current_work_dir, self.data)
        self.vectorizer = vectorizer
        self.dataset_index=dataset_index
        self.threshold=threshold
        self.m=m
        self.fold=fold
    def run(self,sorted=0,crosspro=0):
        if self.m in ["Complete_XGB","Logistic_regression","Random_forest"]:
            X_train, X_test, y_train, y_test = data_utils.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="ablate_project":
            X_train, X_test, y_train, y_test = data_utils_ablate_project.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="ablate_issue":
            X_train, X_test, y_train, y_test = data_utils_ablate_issue.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="ablate_rpt":
            X_train, X_test, y_train, y_test = data_utils_ablate_rpt.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="ablate_label":
            X_train, X_test, y_train, y_test = data_utils_ablate_label.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="ablate_event":
            X_train, X_test, y_train, y_test = data_utils_ablate_event.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="ablate_experience":
            X_train, X_test, y_train, y_test = data_utils_ablate_experience.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="ablate_comment":
            X_train, X_test, y_train, y_test = data_utils_ablate_comment.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="baseline_project":
            X_train, X_test, y_train, y_test = data_utils_baseline_project.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="baseline_issue":
            X_train, X_test, y_train, y_test = data_utils_baseline_issue.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="baseline_rpt":
            X_train, X_test, y_train, y_test = data_utils_baseline_rpt.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="baseline_label":
            X_train, X_test, y_train, y_test = data_utils_baseline_label.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="baseline_event":
            X_train, X_test, y_train, y_test = data_utils_baseline_event.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="baseline_experience":
            X_train, X_test, y_train, y_test = data_utils_baseline_experience.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)
        if self.m=="baseline_comment":
            X_train, X_test, y_train, y_test = data_utils_baseline_comment.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold,sorted,crosspro)  
        if self.m=="Logistic_regression":
            model = LogisticRegression(max_iter=10000)
        elif self.m=="Random_forest":
            model = RandomForestClassifier(n_estimators=10, criterion='gini')
        else:
            model = XGBClassifier(eval_metric=['logloss','auc','error'],use_label_encoder=False)               
        model.fit(X_train,y_train)            
        y_pred = model.predict(X_test)
        y_score=model.predict_proba(X_test)[:,1]
        auc, recall=metrics_util.get_all_metrics(y_test,y_pred,y_score)
        if self.m in ["Logistic_regression","Random_forest"]:
            acc=model.score(X_test,y_test)
        else:
            acc=accuracy_score(y_test,y_pred)
        return auc,acc,recall

def recgfi_diffthres():
    dataset_index=[1,2]
    k=[0,1,2,3,4]
    for index in dataset_index:
        for threshold in k:
            model_name="Complete_XGB"
            auc=0
            acc=0
            recall=0
            for fold in range(10):
                vectorizer = vectorize.Vectorizer('TFIDF', ngram_range=(1, 1))
                model = XGB(vectorizer,index,threshold,model_name,fold)
                a,b,c=model.run()
                auc+=a
                acc+=b
                recall+=c
            path="/Different_threshold"+".csv"
            current_work_dir = os.path.dirname(__file__) 
            path = current_work_dir+path
            if threshold==0:
                if index==1:
                    write_result(path,"ModelType,Threshold,AUC,ACC,Recall,1st_timepoint")
                else:
                    write_result(path,"ModelType,Threshold,AUC,ACC,Recall,2nd_timepoint")
            write_result(path,model_name+","+str(threshold)+","+str(auc/10)+","+str(acc/10)+","+str(recall/10))

def recgfi_timesorted():
    dataset_index=[1,2]
    k=[0,1,2,3,4]
    for index in dataset_index:
        for threshold in k:
            model_name="Complete_XGB"
            auc=0
            acc=0
            recall=0
            for fold in range(10):
                vectorizer = vectorize.Vectorizer('TFIDF', ngram_range=(1, 1))
                model = XGB(vectorizer,index,threshold,model_name,fold)
                sorted=0
                a,b,c=model.run(sorted)
                auc+=a
                acc+=b
                recall+=c
            path="/Time_sorted_dataset"+".csv"
            current_work_dir = os.path.dirname(__file__) 
            path = current_work_dir+path
            if threshold==0:
                if index==1:
                    write_result(path,"ModelType,Threshold,AUC,ACC,Recall,1st_timepoint")
                else:
                    write_result(path,"ModelType,Threshold,AUC,ACC,Recall,2nd_timepoint")
            write_result(path,model_name+","+str(threshold)+","+str(auc/10)+","+str(acc/10)+","+","+str(recall/10))

def recgfi_crosspro():
    dataset_index=[1,2]
    k=[0,1,2,3,4]
    for index in dataset_index:
        for threshold in k:
            model_name="Complete_XGB"
            auc=0
            acc=0
            recall=0
            for fold in range(10):
                vectorizer = vectorize.Vectorizer('TFIDF', ngram_range=(1, 1))
                model = XGB(vectorizer,index,threshold,model_name,fold)
                sorted=0
                crosspro=1
                a,b,c=model.run(sorted,crosspro)
                auc+=a
                acc+=b
                recall+=c
            path="/Cross_projects_dataset"+".csv"
            current_work_dir = os.path.dirname(__file__) 
            path = current_work_dir+path
            if threshold==0:
                if index==1:
                    write_result(path,"ModelType,Threshold,AUC,ACC,Recall,1st_timepoint")
                else:
                    write_result(path,"ModelType,Threshold,AUC,ACC,Recall,2nd_timepoint")
            write_result(path,model_name+","+str(threshold)+","+str(auc/10)+","+str(acc/10)+","+","+str(recall/10))

def recgfi():
    dataset_index=[1,2]
    m1=["Complete_XGB","Logistic_regression","Random_forest","ablate_project","ablate_issue","ablate_rpt","ablate_label",
    "baseline_project","baseline_issue","baseline_rpt",
    "baseline_label"]
    m2=["Complete_XGB","Logistic_regression","Random_forest","ablate_project","ablate_issue","ablate_rpt","ablate_label","ablate_event",
    "ablate_experience","ablate_comment","baseline_project","baseline_issue","baseline_rpt",
    "baseline_label","baseline_event","baseline_experience","baseline_comment"]
    for index in dataset_index:
        if index==1:
            m=m1
        else:
            m=m2
        threshold=0
        for model_name in m:
            auc=0
            acc=0
            recall=0
            for fold in range(10):
                vectorizer = vectorize.Vectorizer('TFIDF', ngram_range=(1, 1))
                model = XGB(vectorizer,index,threshold,model_name,fold)
                a,b,c=model.run()
                auc+=a
                acc+=b
                recall+=c
            path="/Timepoint_"+str(index)+"_threshold_"+str(threshold)+".csv"
            current_work_dir = os.path.dirname(__file__) 
            path = current_work_dir+path
            if model_name=="Complete_XGB":
                write_result(path,"ModelType,Threshold,AUC,ACC,Recall")
            write_result(path,model_name+","+str(threshold)+","+str(auc/10)+","+str(acc/10)+","+","+str(recall/10))



from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

from metrics_util import get_all_metrics
from utils import data_utils
from utils import data_utils_ablate_comment
from utils import data_utils_ablate_event
from utils import data_utils_ablate_experience
from utils import data_utils_ablate_label
from utils import data_utils_ablate_rpt
from utils import data_utils_ablate_issue
from utils import data_utils_ablate_project

from utils import data_utils_baseline_comment
from utils import data_utils_baseline_experience
from utils import data_utils_baseline_issue
from utils import data_utils_baseline_rpt
from utils import data_utils_baseline_project
from utils import data_utils_baseline_label
from utils import data_utils_baseline_event
from utils import data_utils_sorted
from utils import vectorize
def write_result(file, str):
    f = open(file, "a+")
    f.write(str)
    f.close()


class XGB:
    def __init__(self, vectorizer, dataset_index,threshold,m,fold):
        self.data = "/data/dataset"+str(dataset_index)+"_threshold_"+str(threshold)+".pkl"
        self.vectorizer = vectorizer
        self.dataset_index=dataset_index
        self.threshold=threshold
        self.m=m
        self.fold=fold
    def run(self):
        if self.m=="Complete_XGB":
            X_train, X_test, y_train, y_test = data_utils.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="ablate_project":
            X_train, X_test, y_train, y_test = data_utils_ablate_project.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="ablate_issue":
            X_train, X_test, y_train, y_test = data_utils_ablate_issue.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="ablate_rpt":
            X_train, X_test, y_train, y_test = data_utils_ablate_rpt.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="ablate_label":
            X_train, X_test, y_train, y_test = data_utils_ablate_label.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="ablate_event":
            X_train, X_test, y_train, y_test = data_utils_ablate_event.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="ablate_experience":
            X_train, X_test, y_train, y_test = data_utils_ablate_experience.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="ablate_comment":
            X_train, X_test, y_train, y_test = data_utils_ablate_comment.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="baseline_project":
            X_train, X_test, y_train, y_test = data_utils_baseline_project.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="baseline_issue":
            X_train, X_test, y_train, y_test = data_utils_baseline_issue.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="baseline_rpt":
            X_train, X_test, y_train, y_test = data_utils_baseline_rpt.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="baseline_label":
            X_train, X_test, y_train, y_test = data_utils_baseline_label.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="baseline_event":
            X_train, X_test, y_train, y_test = data_utils_baseline_event.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="baseline_experience":
            X_train, X_test, y_train, y_test = data_utils_baseline_experience.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="baseline_comment":
            X_train, X_test, y_train, y_test = data_utils_baseline_comment.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)
        if self.m=="sorted":
            X_train, X_test, y_train, y_test = data_utils_sorted.load_train_test_data(self.data,self.vectorizer,self.dataset_index,fold)        
        model = XGBClassifier()               
        model.fit(X_train,y_train)            
        y_pred = model.predict(X_test)
               
        y_score=model.predict_proba(X_test)[:,1]
       
        
        auc,precision, recall, f1, average_precision, fpr, tpr,ndcg=get_all_metrics(y_test,y_pred,y_score)
        acc=accuracy_score(y_test,y_pred)
        write_result("res"+str(self.dataset_index)+"/threshold_"+str(self.threshold)+".csv",self.m+","+str(self.threshold)+","+str(auc)+","+str(acc)+","+str(precision)+","+str(recall)+","+str(f1)+","+str(ndcg)+",15000,15000\n")


if __name__ == '__main__':
    dataset_index=[1,2]
    k=[1,2,3,4,5]
    m=["Complete_XGB","ablate_project","ablate_issue","ablate_rpt","ablate_label","ablate_event",
    "ablate_experience","ablate_comment","baseline_project","baseline_issue","baseline_rpt",
    "baseline_label","baseline_event","baseline_experience","baseline_comment"]
    for index in dataset_index:
        for threshold in k:
            for model_name in m:
                for fold in range(10):
                    vectorizer = vectorize.Vectorizer('TFIDF', ngram_range=(1, 1))
                    model = XGB(vectorizer,index,threshold,model_name,fold)
                    model.run()


from sklearn.linear_model import LogisticRegression
from metrics_util import get_all_metrics
from utils import data_utils
from utils import vectorize
from utils import numpy as np
def write_result(file, str):
    f = open(file, "a+")
    f.write(str)
    f.close()


class MyLogisticRegression:
    def __init__(self, vectorizer, dataset_index,threshold,fold):
        self.data = "/data/dataset"+str(dataset_index)+"_threshold_"+str(threshold)+".pkl"
        self.vectorizer = vectorizer
        self.dataset_index=dataset_index
        self.threshold=threshold
        self.fold=fold

    def run(self):
        X_train, X_test, y_train, y_test = data_utils.load_train_test_data(self.data,self.vectorizer,self.dataset_index,self.fold)
       
        lr = LogisticRegression(max_iter=10000)
        
        
        lr.fit(X_train, y_train)
        y_pred=lr.predict(X_test)
        y_score=lr.predict_proba(X_test)[:,1]
        
        auc,precision, recall, f1, average_precision, fpr, tpr,ndcg=get_all_metrics(y_test,y_pred,y_score)
        acc=lr.score(X_test,y_test)
        write_result("res"+str(self.dataset_index)+"/threshold_"+str(self.threshold)+".csv",lr.__class__.__name__+","+str(self.threshold)+","+str(auc)+","+str(acc)+","+str(precision)+","+str(recall)+","+str(f1)+","+str(ndcg)+",15000,15000\n")
        


if __name__ == '__main__':
    dataset_index=[2]
    threshold=1
    
    for index in dataset_index:
        for fold in range(10):
            vectorizer = vectorize.Vectorizer('TFIDF', ngram_range=(1, 1))
            model = MyLogisticRegression(vectorizer,index,threshold,fold)
            model.run()

from sklearn.metrics import recall_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc

def get_all_metrics(eval_labels, pred_labels,scores):
    fpr, tpr, thresholds_keras = roc_curve(eval_labels,scores)
    auc_ = auc(fpr, tpr)
    recall = recall_score(eval_labels, pred_labels)
    return auc_, recall
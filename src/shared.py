import numpy as np
from datetime import datetime
from sklearn import metrics
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt


def spectrogram_visualization(image,title=None):
    plt.figure()
    plt.imshow(np.flipud(image.T),interpolation=None)
    plt.colorbar()
    if title!=None:
        plt.title(title)
    else:
        title=str(get_epoch_time())
    plt.savefig(title + '.png')
    

def get_epoch_time():
    return int((datetime.now() - datetime(1970,1,1)).total_seconds())


def count_params(trainable_variables):
    # to return number of trainable variables
    # Example: shared.count_params(tf.trainable_variables()))
    return np.sum([np.prod(v.get_shape().as_list()) for v in trainable_variables])


def load_id2gt(gt_file):
    ids = []
    fgt = open(gt_file)
    id2gt = dict()
    for line in fgt.readlines():
        id, gt = line.strip().split("\t") # id is string
        id2gt[id] = eval(gt) # gt is array
        ids.append(id)
    return ids, id2gt


def load_id2path(index_file):
    paths = []
    fspec = open(index_file)
    id2path = dict()
    for line in fspec.readlines():
        id, path, _ = line.strip().split("\t")
        id2path[id] = path
        paths.append(path)
    return paths, id2path


def auc_with_aggergated_predictions(pred_array, id_array, ids, id2gt): 
    # averaging probabilities -> one could also do majority voting
    y_pred = []
    y_true = []
    for id in ids:
        try:
            avg = np.mean(pred_array[np.where(id_array==id)], axis=0)
            y_pred.append(avg)
            y_true.append(id2gt[id])
        except:
            print(id)
            
    print('Predictions are averaged, now computing AUC..')
    roc_auc, pr_auc = compute_auc(y_true, y_pred)
    return  np.mean(roc_auc), np.mean(pr_auc)


## REMOVE!!! BE SURE IT GIVES EXACTLY THE SAME AS BELOW !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def compute_roc_auc(true, estimated):
    '''
    AUC is computed at the tag level because there are many songs in the MTT having no annotations - zeros array.
    Input dimensions:
    - true: #songs x #annotations    
    - estimated: #songs x #outputNeurons
    where #outputNeurons = #annotations
    '''
    aucs=[]
    estimated = np.array(estimated)
    true = np.array(true)
    for count in range(estimated.shape[1]-1):
        if np.min(true[:,count]) != np.max(true[:,count]):
            auc = metrics.roc_auc_score(true[:,count],estimated[:,count])
            aucs.append(auc)
        else:
            print('WARNING: All 0s or 1s, can not compute AUC! Tag #'+str(count))
    return np.mean(aucs)
   

def compute_auc(true,estimated):
    pr_auc=[]
    roc_auc=[]    
    estimated = np.array(estimated)
    true = np.array(true) 
    for count in range(0,estimated.shape[1]):
        pr_auc.append(metrics.average_precision_score(true[:,count],estimated[:,count]))
        roc_auc.append(metrics.roc_auc_score(true[:,count],estimated[:,count]))
    return roc_auc, pr_auc


# -*- coding: utf-8 -*-

import numpy as np
import keras
import os
import pickle
import h5py
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc
from scipy import interp

def scnn(model, test_data):
    scnn_pred = model.predict(test_data, batch_size=3, verbose=1)
    scnn_predicted = np.argmax(scnn_pred, axis=1)
    return scnn_pred, scnn_predicted

#a, b = scnn(model, test_data)

def generarDicts(n_classes, test_labels_one_hot, scnn_pred):
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(test_labels_one_hot[:, i], scnn_pred[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    return fpr, tpr, roc_auc


#c ,d ,e = generarDicts(3,test_labels_one_hot,a)

# Compute micro-average ROC curve and ROC area
def compuMicro(fpr, tpr, roc_auc, test_labels_one_hot, scnn_pred):
    fpr["micro"], tpr["micro"], _ = roc_curve(test_labels_one_hot.ravel(), scnn_pred.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    print(roc_auc["micro"])
    return fpr["micro"], tpr["micro"] , roc_auc["micro"]

#f , g , h =compuMicro(c,d,e,test_labels_one_hot, a)


def generarAllMean(fpr, tpr, n_classes):
    # First aggregate all false positive rates
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

    # Then interpolate all ROC curves at this points
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(n_classes):
        mean_tpr += interp(all_fpr, fpr[i], tpr[i])

    # Finally average it and compute AUC
    mean_tpr /= n_classes
    return all_fpr, mean_tpr


def generarMacro(all_fpr, mean_tpr, fpr, tpr, roc_auc):
    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
    return roc_auc["macro"], fpr["macro"], tpr["macro"]

def generate_predict_classes(model, test_data_images):
    yhat_classes_l = []
    for k in range(test_data_images.shape[0]):
        img = np.expand_dims(test_data_images[k],axis=0)
        a = model.predict(img)
        result = np.where(a[0] == np.amax(a[0]))
        pred = result[0][0]
        yhat_classes_l.append(pred)
    yhat_classes = np.array(yhat_classes_l)
    return yhat_classes

def save_metrics(fprMicro, tprMicro, fprMacro, tprMacro, auc_values, report_values):
    with h5py.File("/folder/code/static/metrics/metrics_own_model.h5",'w') as hdf:
        hdf.create_dataset('fprMicro', data=fprMicro)
        hdf.create_dataset('tprMicro', data=tprMicro)
        hdf.create_dataset('fprMacro', data=fprMacro)
        hdf.create_dataset('tprMacro', data=tprMacro)
        hdf.create_dataset('aucValues', data=auc_values)
        hdf.create_dataset('reportValues', data=report_values)

def generate_metrics(model, test_data, test_target, test_target_list, test_data_images):
    scnn_pred, scnn_predicted = scnn(model, test_data)
    fpr, tpr, roc_auc = generarDicts(8, test_target, scnn_pred)
    fprMicro, tprMicro, rocMicro = compuMicro(fpr, tpr, roc_auc, test_target, scnn_pred)
    all_fpr, mean_tpr = generarAllMean(fpr, tpr, 8)
    rocMacro, fprMacro, tprMacro = generarMacro(all_fpr, mean_tpr, fpr, tpr, roc_auc)
    predicted_classes = generate_predict_classes(model, test_data_images)
    precision = precision_score(test_target_list, predicted_classes, average = 'micro')
    recall = recall_score(test_target_list, predicted_classes, average = 'micro')
    f1 = f1_score(test_target_list, predicted_classes, average = 'micro')
    kappa = cohen_kappa_score(test_target_list, predicted_classes)
    auc_values = np.array([rocMicro,rocMacro])
    report_values = np.array([precision,recall,f1,kappa])
    save_metrics(fprMicro, tprMicro, fprMacro, tprMacro, auc_values, report_values)

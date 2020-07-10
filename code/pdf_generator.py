# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
import h5py
from skimage import io, transform
import os
from fpdf import FPDF

path_base = "/folder/code/static/metrics/"

def load_metrics_data_roc(array_models):
    array_fpr_micro = []
    array_tpr_micro = []
    array_fpr_macro = []
    array_tpr_macro = []
    for i in range(len(array_models)):
        with h5py.File(path_base+'metrics_'+array_models[i]+'.h5','r') as hdf:
            fprMicro_data = hdf.get('fprMicro')
            fprMicro = np.array(fprMicro_data)
            tprMicro_data = hdf.get('tprMicro')
            tprMicro = np.array(tprMicro_data)
            fprMacro_data = hdf.get('fprMacro')
            fprMacro = np.array(fprMacro_data)
            tprMacro_data = hdf.get('tprMacro')
            tprMacro = np.array(tprMacro_data)
        array_fpr_micro.append(fprMicro)
        array_tpr_micro.append(tprMicro)
        array_fpr_macro.append(fprMacro)
        array_tpr_macro.append(tprMacro)
    return array_fpr_micro, array_tpr_micro, array_fpr_macro, array_tpr_macro


def load_metrics_data_report(array_models):
    array_report_values = []
    header = ['Model', 'AUC', 'Precision score', 'Recall Score', 'F1 Score', 'Kappa Coeff.']
    array_report_values.append(header)
    for i in range(len(array_models)):
        array_temp = []
        with h5py.File(path_base+'metrics_'+array_models[i]+'.h5','r') as hdf:
            aucc_data = hdf.get('aucValues')
            auct = np.array(aucc_data)
            report_data = hdf.get('reportValues')
            report = np.array(report_data)
        array_temp.extend([array_models[i],str(round(np.mean(auct),4)),str(round(report[0],4)),str(round(report[1],4)),str(round(report[2],4)),str(round(report[3],4))])
        array_report_values.append(array_temp)
    return array_report_values


def generate_graphs_macro(array_models,array_fpr_macro, array_tpr_macro):
    ruta_macro = '/folder/code/static/results/files/roc_macro.png'
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(len(array_models)):
       ax.plot(array_fpr_macro[i], array_tpr_macro[i], '--')
    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_title("ROC Curve Macro")
    ax.set_ylabel('True Positive Rate')
    ax.set_xlabel('False Positive Rate')
    ax.legend(array_models)
    fig.savefig(ruta_macro)
    return ruta_macro

def generate_graphs_micro(array_models,array_fpr_micro, array_tpr_micro):
    ruta_micro = '/folder/code/static/results/files/roc_micro.png'
    fig2 = plt.figure()
    ax1 = fig2.add_subplot(111)
    for i in range(len(array_models)):
       ax1.plot(array_fpr_micro[i], array_tpr_micro[i], '--')
    ax1.plot([0, 1], [0, 1], 'k--')
    ax1.set_xlim([0.0, 1.0])
    ax1.set_ylim([0.0, 1.05])
    ax1.set_title("ROC Curve Micro")
    ax1.set_ylabel('True Positive Rate')
    ax1.set_xlabel('False Positive Rate')
    ax1.legend(array_models)
    fig2.savefig(ruta_micro)
    return ruta_micro

def generate_pdf(ruta_micro, ruta_macro, report_values):
    pdf = FPDF(format='A4')
    pdf.set_left_margin(margin = 20)
    pdf.set_right_margin(margin = 20)
    pdf.set_top_margin(margin = 20)
    pdf.add_page()
    pdf.set_font("times", size=24, style='B')
    pdf.cell(168, 20, txt="Comparison Results", align="C", ln=2)
    pdf.line(60, 35, 145, 35)
    pdf.ln(5)
    pdf.set_font('Times','',10.0)
    loremipsum = """This document is intended to present the results of the comparison process between selected convolutional neural network models. For the evaluation of the models, metrics such as: ROC Curve, Precision Score, Recall Score, F1 Score and Kappa Coeffiecient were taken into account. Additionally, a total of 1239 images were used, distributed in 8 classes: Airplane, Airport, Commercial Area, Forest, Freeway, Island, Ship and Stadium. These images were taken from the NWPU-RESISC45 dataset"""
    pdf.multi_cell(0, 5, loremipsum, align = 'J')
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.cell(0, 5, txt = "Cuvas de ROC")
    pdf.ln(7)
    loremipsum_2 = """A receiver operating characteristic curve or ROC curve is considered as a factor commonly used to determine the level of precision in multi-classifier models."""
    pdf.set_font('Times','',10.0)
    pdf.multi_cell(0, 5, loremipsum_2, align = 'J')
    pdf.ln(10)
    pdf.set_font('Times','B',12.0)
    pdf.cell(0, 5, txt = "Macro ROC")
    #pdf.ln(7)
    #loremipsum_2 = """Lorem ipsum dolor sit amet, vel ne quando dissentias. Ne his opo at expetendis. Ei tantas explicari quo, sea vidit minimum menandri ea. His case errem."""
    #pdf.set_font('Times','',10.0)
    #pdf.multi_cell(0, 5, loremipsum_2, align = 'J')
    pdf.ln(5)
    pdf.image(ruta_macro,x=20,w=170,h=120)
    pdf.ln(50)
    pdf.set_font('Times','B',12.0)
    pdf.cell(0, 5, txt = "Micro ROC")
    #pdf.ln(7)
    #loremipsum_2 = """Lorem ipsum dolor sit amet, vel ne quando dissentias. Ne his opo at expetendis. Ei tantas explicari quo, sea vidit minimum menandri ea. His case errem."""
    #pdf.set_font('Times','',10.0)
    #pdf.multi_cell(0, 5, loremipsum_2, align = 'J')
    pdf.ln(5)
    pdf.image(ruta_micro,x=20,w=170,h=120)
    pdf.ln(10)
    pdf.set_font('Times','B',14.0)
    pdf.cell(0, 5, txt = "Report Classification")
    pdf.ln(7)
    loremipsum_2 = """This section presents the evaluation of the models using metrics such as Precision Score, F1 Score, Recall Score, the average of the macro and micro Roc curve, denoted as Area Under Curve (AUC) and Kappa Coefficient."""
    pdf.set_font('Times','',10.0)
    pdf.multi_cell(0, 5, loremipsum_2, align = 'J')
    pdf.ln(7)
    loremipsum_2 = """Precision is the ability of a classifier not to label an instance positive that is actually negative. For each class it is defined as the ratio of true positives to the sum of true and false positives."""
    pdf.set_font('Times','',10.0)
    pdf.multi_cell(0, 5, loremipsum_2, align = 'J')
    pdf.ln(7)
    loremipsum_2 = """Recall is the ability of a classifier to find all positive instances. For each class it is defined as the ratio of true positives to the sum of true positives and false negatives."""
    pdf.set_font('Times','',10.0)
    pdf.multi_cell(0, 5, loremipsum_2, align = 'J')
    pdf.ln(7)
    loremipsum_2 = """The F1 score is a weighted harmonic mean of precision and recall such that the best score is 1.0 and the worst is 0.0. Generally speaking, F1 scores are lower than accuracy measures as they embed precision and recall into their computation. As a rule of thumb, the weighted average of F1 should be used to compare classifier models, not global accuracy."""
    pdf.set_font('Times','',10.0)
    pdf.multi_cell(0, 5, loremipsum_2, align = 'J')
    pdf.ln(10)
    pdf.set_font('Times','',10.0)
    spacing = 1
    col_width = pdf.w / 8
    row_height = pdf.font_size + 1
    for row in report_values:
    	for item in row:
    		pdf.cell(col_width, row_height*spacing,txt=item, border=1)
    	pdf.ln(row_height*spacing)
    pdf.output("/folder/code/static/results/files/results.pdf")

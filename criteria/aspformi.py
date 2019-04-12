#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 10:37:54 2018

@author: nalingna
"""
import re
from os import listdir

def asp(content):
    asp_lst = ['asa', 'aspirin', 'acetylsalicylic acid']
    content = content.lower()  
    mentioned_asp = []
    for pattern in asp_lst:
        pattern = '\\b' + pattern + '\\b'
        m = re.findall(pattern, content)   
        if m:
            mentioned_asp.append(m[0])
    
    if mentioned_asp:
        outcome = 'met'
    else:
        outcome = 'not met'
    return outcome

def proc():
    # get all files from the train folder
    filelist = listdir('/Users/nalingna/Desktop/n2c2/train/')
    # call the function (search_asp) and write my outcome into a list (outcomelist)
    prediction_list = [search_asp(i) for i in filelist]

    # <ASP-FOR-MI met="not met" />

    # combine the filename and its corresponding prediction
    aa = list(zip(filelist, prediction_list))
    # remove the ".xml" from the filename
    filelistnum = [i.replace('.xml', '') for i in filelist]

    # Open the output file
    resultFile = open("/Users/nalingna/Desktop/n2c2/output.csv",'w')
    resultFile.write('file' + ',' + 'ASP-FOR-MI-PREDICTED' + "\n")
    # Write data to file
    for r in range(len(filelist)):
        resultFile.write(filelistnum[r] + ',' + prediction_list[r] + "\n")
    resultFile.close()

    # read in the true outcome file and save the true result in a list (trueoutcomelist)
    trueoutcome_list = []
    labelFile = open('/Users/nalingna/Desktop/n2c2/trainLabels.csv', 'r')
    labelFile.readline()
    for line in labelFile.readlines():
        array = line.split(',')
        trueoutcome_list.append(array[4])
    labelFile.close()

    # compare prediction and true outcome [asp-for-mi] 
    outcomematch = [prediction_list[i] == trueoutcome_list[i] for i in range(len(prediction_list))]
    sum(outcomematch) / len(outcomematch)

    # with asa: 84%
    # without asa: 82%
    # most urgent issue: failed to find a lot of "not met" cases

    # Open the output file for asp-for-mi 
    compared = open("/Users/nalingna/Desktop/n2c2/compared.csv",'w')
    compared.write('file' + ',' + 'PREDICTED' + ',' + 'True Result' + "\n")
    # Write data to file
    for r in range(len(filelist)):
        compared.write(filelistnum[r] + ',' + prediction_list[r] + ',' + trueoutcome_list[r] + "\n")
    compared.close()


    # Evaluation 

    # True positive = predicted positive / actual positive
    # False negative = predicted negative / actual negative 
    # False positive = predicted positive / actual negative 
    # True negative = predicted negative / actual negative 


    def perf_measure(y_actual, y_hat):
        TP = 0
        FP = 0
        TN = 0
        FN = 0
        for i in range(len(y_hat)): 
            if y_actual[i] == y_hat[i] == 'met':
               TP += 1
            if y_hat[i] == 'met' and y_actual[i] != y_hat[i]:
               FP += 1
            if y_actual[i] == y_hat[i] == 'not met':
               TN += 1
            if y_hat[i] == 'not met' and y_actual[i]!=y_hat[i]:
               FN += 1
        print("TP = " + str(TP), "FP = " + str(FP) ,"TN = " + str(TN),"FN = " + str(FN))
        return(TP, FP, TN, FN)

    
    pm = perf_measure(trueoutcome_list, prediction_list)

    # accuracy = (ture positive + true negative) / all pop
    # specificity = TNR
    sensitivity = round(pm[0] / (pm[0] + pm[3]),2)
    precision = round(pm[0]  / (pm[0] + pm[1]),2)
    specificity = round(pm[1] / (pm[1] + pm[2]), 2)
    f1_score = round((2 * precision * sensitivity) / (precision + sensitivity) , 2)

    print("sensitivity = " + str(sensitivity))
    print("precision = " + str(precision))
    print("specificity = " + str(specificity))
    print("f1_score = " + str(f1_score))








# PyCon ACPC 2014
# Zhan Yuli
# Code reference
# 1)Peter Harrington - Data Mining in Action
# 2)http://blog.csdn.net/v_july_v/article/details/7624837
# 3)http://blog.csdn.net/aichipmunk/article/details/9382503


import time
from preprocessing import *
import matplotlib.pyplot as plt
import numpy as np
import random

# linear regression
# using Sigmoid function as classifier

def loadDataSet():
    dataMat = []
    labelMat = []
    for s in stinfo:
        if s.get_classification() != -1:
            overall = s.show_overall()
            label = s.get_classification()
            for i in range(len(overall)):
                dataMat.append([1.0,float(i),float(overall[i])])
                if label == 0:
                    labelMat.append(0)
                else:
                    labelMat.append(1)
                #print([1.0,float(i),float(overall[i])],label)
    #print(dataMat,labelMat)
    return dataMat,labelMat

def sigmoid(inX):
    #print(inX)
    return 1.0/(1+np.exp(-inX))

def gradAscent(dataMatIn, classLabels):
    dataMatrix = np.mat(dataMatIn) 
    labelMat = np.mat(classLabels).transpose()
    m,n = np.shape(dataMatrix)
    alpha = 0.001
    maxCycles = 200000
    weights = np.ones((n,1))
    # stability test
    x0 = []; x1 = []; x2 = [];
    y = []
    for k in range(maxCycles):
        if(k%10000==0):
            print("Cycle",k)
            print("weight len",len(weights))
            print(np.array(weights[0])[0])
            x0.append(np.array(weights[0])[0])
            x1.append(np.array(weights[1])[0])
            x2.append(np.array(weights[2])[0])
            y.append(k)
        h = sigmoid(dataMatrix*weights) 
        error = (labelMat - h)              
        weights = weights + alpha * dataMatrix.transpose()* error
    '''
    #Plot fluctation trend of weight value
    fig = plt.figure()
    ax = fig.add_subplot(311)
    print("x1",len(x1),"x2",len(x2),"x0",len(x0),"y",len(y))
    print(x1)
    print(y)
    ax.plot(y,x0)
    bx = fig.add_subplot(312)
    bx.plot(y,x1)
    cx = fig.add_subplot(313)
    cx.plot(y,x2)
    plt.show()
    '''
    return weights

def plotBestFit(wei):
    global stinfo
    print("Ploting best-fit")
    weights = wei.getA()
    
    '''
    # Plot data points
    t = []
    for s in stinfo:
        # if classification data present
        if(s.get_classification != -1):
            y = s.show_overall()
            x = np.arange(0,len(y),1)
            # print(s.get_classification())
            if s.get_classification() == 0:
                plt.plot(x,list(map((lambda x:x),y)),"y",alpha=0.4,linewidth=0.5)
            else:
                plt.plot(x,list(map((lambda x:x),y)),"k",alpha=0.4,linewidth=0.5)
    '''
    dataMat,labelMat=loadDataSet()
    dataArr = np.array(dataMat)
    n = np.shape(dataArr)[0] 
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(xcord1, ycord1, "m",linewidth = 1.0)
    plt.plot(xcord2, ycord2, "c",linewidth = 1.0)            
    x = np.arange(0.0, 6.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    print(x,y)
    ax.plot(x, y,"k",linewidth = 4.0)
    plt.xlabel('Time')
    plt.ylabel('Ranking')
    plt.show()


data, label = loadDataSet()
weights = gradAscent(data,label)
print(plotBestFit(weights))

# PyCon ACPC 2014
# Zhan Yuli
# Code reference
# 1)Peter Harrington - Data Mining in Action

import time
from dhs_preprocessing import *
import matplotlib.pyplot as plt
from numpy import *
from functools import reduce

scatterMarkers=['s', 'o', '^','p', \
                    'd', 'v', 'h', '>', '<','8']

scatterColours = ["r","b","g","c","m","y","k"]

grade2num = {"A":20,
             "B":17.5,
             "C":15,
             "D":12.5,
             "E":10,
             "S":5,
             "U":0,}

def loadDataSet(fileName): 
    dataMat = [] 
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine)
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2))) 

def randCent(dataSet, k):
    n = np.shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    #create random cluster centers
    for j in range(n):
        minJ = min(dataSet[:,j]) 
        rangeJ = float(max(dataSet[:,j]) - minJ)
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
    return centroids
    
def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    #create mat to assign data points 
    #to a centroid, also holds SE of each point
    clusterAssment = mat(zeros((m,2)))
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        #for each data point assign it to the closest centroid
        for i in range(m):
            minDist = inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print(centroids)
        #recalculate centroids
        for cent in range(k):
            #get all the point in this cluster
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
            #assign centroid to mean
            centroids[cent,:] = mean(ptsInClust, axis=0)  
    return centroids, clusterAssment


def select_sub(sub1,sub2,dataset,numClust):
    count = 0
    x = []
    y = []
    result = []
    plt.xlabel(sub1)
    plt.ylabel(sub2)
    for st in dataset:
        select_1 = False
        select_2 = False
        result_1 = []
        result_2 = []
        nextSub = st.getSubject()
        while nextSub:
            if nextSub.getCode() == sub1:
                select_1 = True
                result_1 = [grade2num[x] for x in nextSub.getScore()]
            elif nextSub.getCode() == sub2:
                select_2 = True
                result_2 = [grade2num[x] for x in nextSub.getScore()]
            nextSub = nextSub.getNext()
        if select_1 and select_2:
            count += 1
            average_1 = reduce(lambda x, y: x + y, result_1) / len(result_1)
            average_2 = reduce(lambda x, y: x + y, result_2) / len(result_2)
            #print(average_1,average_2)
            x.append(average_1)
            y.append(average_2)
            result.append([average_1,average_2])
    #plt.scatter(x,y)
    #plt.show()
    datMat = mat(result)
    myCentroids, clustAssing = kMeans(datMat, numClust)

    for i in range(numClust):
        ptsInCurrCluster = datMat[nonzero(clustAssing[:,0].A==i)[0],:]
        markerStyle = scatterMarkers[i % len(scatterMarkers)]
        colourStyle = scatterColours[i % len(scatterColours)]
        plt.scatter(ptsInCurrCluster[:,0].flatten().A[0], ptsInCurrCluster[:,1].flatten().A[0],c = colourStyle, marker=markerStyle, s=200)
    plt.scatter(myCentroids[:,0].flatten().A[0], myCentroids[:,1].flatten().A[0], marker='+', s=300)
    plt.show()
    return result
            



#select_sub("H2ECONS","H2MATH",stinfo,5)
select_sub("H2ECONS","H2MATH",stinfo,10)

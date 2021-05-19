import csv
import sys
import numpy as np
import random

def RSS(actual,predition):
    sum=0
    for x in range(100):
        sum+=((predition[x]-actual[x])**2)
    return sum

def Rsquared(actual,predition):
    totalVar=0
    avg=0
    for x in range(100):
        avg+=actual[x]
    avg/=99
    for x in range(100):
        totalVar+=((actual[x]-avg)**2)
    return 1-(RSS(actual,predition)/totalVar)

def getRsquared(FileToReadFrom,polyOrder):

    with open(FileToReadFrom, 'r') as readFrom:
        reader=csv.reader(readFrom.readlines())
        xValues=[]
        yValues=[]
        maxVal=-1.0
        minVal=2.0
        subCount=float(0)
        for line in reader:
            xValues.append(subCount)
            yValues.append(float(line[8]))
            if maxVal<float(line[8]):
                maxVal=float(line[8])
            if minVal>float(line[8]):
                minVal=float(line[8])
            subCount+=.001
        valueRange=maxVal-minVal
        scalledY=[]
        for y in yValues:
            scalledY.append(-1+(((y-minVal)*2)/(valueRange)))
        np.reshape(xValues,newshape=(len(xValues)))
        np.reshape(scalledY,newshape=(len(scalledY)))
        curve_fit = np.polyfit(xValues, scalledY, polyOrder)
        polynomials=[]
        polyCount=polyOrder
        for x in curve_fit:
            polynomials.append([polyCount,x])
            polyCount-=1
        regressionY=[]
        for x in range(100):
            regressionY.append(float(0))
            for scale in polynomials:
                regressionY[x]+=scale[1]*(x/1000.0)**scale[0]
    return Rsquared(scalledY,regressionY)

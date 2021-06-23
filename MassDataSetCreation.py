import sys
import numpy as np
import time
import csv
import datetime
import random
from DataSetCreation import *

#continusly calls createDataSet and saves it to dataLines
#the prints are there to check on progress
dataSetNum=5
dataLines=[]
while dataSetNum<600:
    data=createDataSet("PersonalEURtoUSD5m.csv",8,dataSetNum,.03)
    if isinstance(data,np.ndarray):
        dataLines.append(data)
        print("Data Written on set: "+str(dataSetNum))
    dataSetNum+=1
    print(str(dataSetNum))
#shuffle the data around so its not in cronological order
random.shuffle(dataLines)
#save it
with open('20188Poly.03Xstep.csv', 'w', newline='') as writeTo:
    writer=csv.writer(writeTo)
    for line in dataLines:
        writer.writerow(line)
#scale and normalize the polynomial coefficents and save it to a new file
with open('2018Scalled8Poly.03Xstep.csv', 'w', newline='') as writeTo:
    writer=csv.writer(writeTo)
    for line in dataLines:
        maxVal=-1000000
        minVal=1000000
        row=[]
        for values in line[:9]:
            if values>maxVal:
                maxVal=values
            if values<minVal:
                minVal=values
        inputRange=maxVal-minVal
        for values in line[:9]:
            row.append(round((-10+(((float(values)-minVal)*20)/(inputRange))),2))
        row.append(line[9])
        row.append(line[10])
        writer.writerow(row)

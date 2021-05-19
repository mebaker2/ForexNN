import csv
import sys
import numpy as np
import random
from R2checking import *

polySum=[0.0]

for dataSetNum in range(1,1001):
    with open('EUR_USD_5M.csv', 'r') as readFrom:
        reader=csv.reader(readFrom.readlines())
    with open('DataPoints.csv', 'w', newline='') as writeTo:
        writer=csv.writer(writeTo)
        startNum=random.randrange(6,1000000)
        endNum=startNum+100
        count=0
        subCount=float(0)
        for row in reader:
            if count>startNum and count<=endNum:
                writer.writerow(row)
            count+=1
            if count>endNum+1:
                break
    for polynomialOrder in range(1,16):
        polySum.append(0.0)
        polySum[polynomialOrder]+=getRsquared("DataPoints.csv",polynomialOrder)
    print("data set: "+str(dataSetNum))
for polynomialOrder in range(1,16):
    print("For polyOrder "+str(polynomialOrder)+":we have R2 of: "+str(polySum[polynomialOrder]/1001))

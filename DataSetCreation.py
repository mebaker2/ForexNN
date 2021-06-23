import sys
import numpy as np
import time
import csv
import datetime
import random
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

#filename is the file to read from and for this purpose is csv where each line is a 5m interval of a forexpair
#polySize is the polynomial degreee you wish to fit to the data
#offset is how many days from "firstTime" to try and get the data for the day
#xStep is how much to increse the x value for the data that is being generated and will affect the outcome of the polynomial fitting
def createDataSet(filename,polySize,offset,xStep):
    #firstTime needs to be an epoch that is equvilant to 10pm GMT time
    #jan 1st 2008
    firstTime=1199397600
    #jan 1st 2018
    firstTime=1515016800
    #get what ever day is next and make sure its not a saturday
    day=(offset*86400)
    day+=firstTime
    englishDate=time.strftime("%a",time.gmtime(day))
    if englishDate=="Sat":
        return "Bad Data"
    #pull the data from csv file and load it into storedLines
    storedLines=[]
    with open(filename, 'r') as readFrom:
        reader=csv.reader(readFrom.readlines()[(17260*offset):])
        lineNum=0
        linesToPrint=248
        printing=False
        for input in reader:
            if int(input[0]) == day:
                printing=True
            if printing and linesToPrint>0:
                linesToPrint-=1
                storedLines.append(input)
            if linesToPrint == 0:
                break
            lineNum+=1
        #make sure we have to proper data
        if linesToPrint>0 or not(int(storedLines[247][0])==(day+74100)):
            return "Bad Data"
        #storage of the important parts of the data pulled from the day
        inputX=[]
        inputY=[]
        subCount=0.0
        maxValin=-1.0
        minValin=3.0
        count=0
        start=0.0
        end=0.0
        for row in storedLines:
            if count==128:
                start=float(row[1])
            if count==247:
                end=float(row[1])
            if count<128:
                inputX.append(round(subCount,4))
                inputY.append(float(row[8]))
                if maxValin<float(row[8]):
                    maxValin=float(row[8])
                if minValin>float(row[8]):
                    minValin=float(row[8])
            subCount+=xStep
            count+=1
        #scalling/normalization of the input
        inputRange=maxValin-minValin
        scalledYinput=[]
        percentChange=((end-start)/start)*100
        for y in inputY:
            scalledYinput.append(-1+(((y-minValin)*2)/(inputRange)))

        #numpy arrays are cooler and i should get better at making sure i start with np arrays
        np.reshape(inputX,newshape=(len(inputX)))
        np.reshape(scalledYinput,newshape=(len(scalledYinput)))

        #polynomial fitting and adding the change for the day and if the day should be shorted(0) or long(1)
        curve_fitInput=np.polyfit(inputX,scalledYinput,polySize)
        curve_fitInput=np.insert(curve_fitInput,polySize+1,percentChange)
        if percentChange>0:
            curve_fitInput=np.insert(curve_fitInput,polySize+2,1.0)
        else:
            curve_fitInput=np.insert(curve_fitInput,polySize+2,0.0)
        return curve_fitInput

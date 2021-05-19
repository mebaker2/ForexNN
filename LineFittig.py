import csv
import sys
import numpy as np
import random
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

#varrible creation
xValues=[]
yValues=[]
maxVal=-1.0
minVal=2.0
with open('EUR_USD_5M.csv', 'r') as readFrom:
    reader=csv.reader(readFrom.readlines())
    #rough range of avalible dates since im polling 100 dates, pick one at random
    startNum=random.randrange(6,1000000)
    endNum=startNum+100
    count=0
    subCount=float(0)
    open=[]
    close=[]
    low=[]
    high=[]
    xTime=[]
    for row in reader:
        if count>startNum and count<=endNum:
            #once were in range of my generated date start saving the data
            xValues.append(subCount)
            yValues.append(float(row[8]))
            open.append(row[1])
            high.append(row[2])
            low.append(row[3])
            close.append(row[4])
            xTime.append(subCount)
            #get a minimum and max value for scaling data
            if maxVal<float(row[8]):
                maxVal=float(row[8])
            if minVal>float(row[8]):
                minVal=float(row[8])
            subCount+=.001
        count+=1
        if count>endNum+1:
            break
#scale my closing value tto be between -1 and 1
valueRange=maxVal-minVal
scalledY=[]
for y in yValues:
    scalledY.append(-1+(((y-minVal)*2)/(valueRange)))
#reformat data to numpy arrays for curve fit
np.reshape(xValues,newshape=(len(xValues)))
np.reshape(scalledY,newshape=(len(scalledY)))
polyCountMaster=15
curve_fit = np.polyfit(xValues, scalledY, polyCountMaster)
curve_fit2 = np.polyfit(xValues, scalledY, 8)
curve_fit3 = np.polyfit(xValues, scalledY, 5)
#was an atempt to trim unessacry high order polynomials when i was testing fits, probably needs to be deleted as isnt normaly used
allPlot = make_subplots(rows=2,cols=3,subplot_titles=("Candle","SMA5 Closing","Poly15","","Poly8","Poly5"))
allPlot.add_trace(go.Candlestick(x=xTime,open=open,high=high,low=low,close=close),row=1,col=1)
allPlot.add_trace(go.Scatter(x=xValues,y=scalledY),row=1,col=2)

polynomials=[]
polyCount=15
for x in curve_fit:
    if abs(x)<=.00001:
        print("deleted order:"+str(polyCount))
    else:
        polynomials.append([polyCount,x])
    polyCount-=1
regressionY=[]
for x in range(100):
    regressionY.append(float(0))
    for scale in polynomials:
        regressionY[x]+=scale[1]*(x/1000.0)**scale[0]
allPlot.add_trace(go.Scatter(x=xValues,y=regressionY),row=1,col=3)


polynomials=[]
polyCount=8
for x in curve_fit2:
    if abs(x)<=.00001:
        print("deleted order:"+str(polyCount))
    else:
        polynomials.append([polyCount,x])
    polyCount-=1
regressionY=[]
for x in range(100):
    regressionY.append(float(0))
    for scale in polynomials:
        regressionY[x]+=scale[1]*(x/1000.0)**scale[0]
allPlot.add_trace(go.Scatter(x=xValues,y=regressionY),row=2,col=2)

polynomials=[]
polyCount=5
for x in curve_fit3:
    if abs(x)<=.00001:
        print("deleted order:"+str(polyCount))
    else:
        polynomials.append([polyCount,x])
    polyCount-=1
regressionY=[]
for x in range(100):
    regressionY.append(float(0))
    for scale in polynomials:
        regressionY[x]+=scale[1]*(x/1000.0)**scale[0]
allPlot.add_trace(go.Scatter(x=xValues,y=regressionY),row=2,col=3)
#new Graph with my generated eq
allPlot.update_layout(height=1000, width=1500,title_text="all plots")
allPlot.show()

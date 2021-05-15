import sys
import csv
from collections import deque

count=0
#queue to handle the rolling 14 day percent chnages in RSI calculation
changeLog=deque()
#opening files
with open('EUR_USD_D_DATA.csv', 'r') as readFrom:
    reader=csv.reader(readFrom.readlines())
with open("EUR_USD_D_DATAwRSI.csv", 'w', newline='') as writeTo:
    writer=csv.writer(writeTo)
    for line in reader:
        if count<14:
            writer.writerow(line)
        else:
            #RSI maths
            positiveCount=0.0
            negativeCount=0.0
            positiveSum=0.0
            negativeSum=0.0
            for change in changeLog:
                if float(change)>0:
                    positiveCount+=1.0
                    positiveSum+=float(change)
                else:
                    negativeCount+=1.0
                    negativeSum+=float(change)
                if positiveCount==0:
                    positiveCount=1.0
                if negativeCount==0:
                    negativeCount=1.0
            positiveAvg=positiveSum/positiveCount
            negativeAvg=negativeSum/negativeCount
            if float(line[7])>0:
                if negativeAvg!=0:
                    rsi=100-(100/(1+((positiveAvg*13)+float(line[7]))/((negativeAvg*(-13)))))
                else:
                    #edge cases for 14 up days
                    rsi=100
            else:
                if negativeAvg!=0:
                    rsi=100-(100/(1+((positiveAvg*13)+float(line[7]))/((negativeAvg*(-13)))))
                else:
                    #or 14 down days
                    rsi=0
            line[18]=rsi
            #line writing, queue popping first line skiping part of the code
            changeLog.popleft()
            writer.writerow(line)
        if count!=0:
            changeLog.append(line[7])
        count+=1

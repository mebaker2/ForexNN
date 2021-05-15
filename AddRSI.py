import sys
import csv
from collections import deque

def isNum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

count=0
changeLog=deque()
print("orginal"+str(changeLog))
with open('EUR_USD_D_DATA.csv', 'r') as readFrom:
    reader=csv.reader(readFrom.readlines())
with open("EUR_USD_D_DATAwRSI.csv", 'w', newline='') as writeTo:
    writer=csv.writer(writeTo)
    for line in reader:
        if count<14:
            writer.writerow(line)
            print("BAD WRITE")
        else:
            positiveCount=0.0
            negativeCount=0.0
            positiveSum=0.0
            negativeSum=0.0
            for change in changeLog:
                if float(change)>0:
                    positiveCount+=1.0
                    positiveSum+=float(change)
                    print(str(change)+" has been added new sum is"+str(positiveSum))
                else:
                    negativeCount+=1.0
                    negativeSum+=float(change)
                if positiveCount==0:
                    positiveCount=1.0
                if negativeCount==0:
                    negativeCount=1.0
            positiveAvg=positiveSum/positiveCount
            negativeAvg=negativeSum/negativeCount
            print(positiveAvg)
            print(negativeAvg)
            if float(line[7])>0:
                if negativeAvg!=0:
                    rsi=100-(100/(1+((positiveAvg*13)+float(line[7]))/((negativeAvg*(-13)))))
                else:
                    rsi=100
            else:
                if negativeAvg!=0:
                    rsi=100-(100/(1+((positiveAvg*13)+float(line[7]))/((negativeAvg*(-13)))))
                else:
                    rsi=0
            line[18]=rsi
            changeLog.popleft()
            writer.writerow(line)
        if count!=0:
            changeLog.append(line[7])
        print(changeLog)
        count+=1

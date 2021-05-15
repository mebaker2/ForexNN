import sys
import csv

def isNum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

count=0
with open('CSVs/EUR_USD_D.csv', 'r') as readFrom:
    reader=csv.reader(readFrom.readlines())
with open("EUR_USD_D_DATA.csv", 'w', newline='') as writeTo:
    writer=csv.writer(writeTo)
    for line in reader:
        if count<12:
            writer.writerow(line)
        elif count<26:
            line[16]=(float(line[4])*(2/(13)))+(prevEMA12*(1-(2/13)))
            writer.writerow(line)
        else:
            line[16]=round( (float(line[4])*(2/(13)))+(prevEMA12*(1-(2/13))), 5)
            line[17]=round( (float(line[4])*(2/(26)))+(prevEMA26*(1-(2/26))), 5)
            writer.writerow(line)
        if isNum(line[16]):
            prevEMA12=float(line[16])
        if isNum(line[17]):
            prevEMA26=float(line[17])
        count+=1

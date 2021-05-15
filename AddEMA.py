import sys
import csv

#little function to help with not adding the #N/A values in my maths
def isNum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

count=0
#open my files
with open('CSVs/EUR_USD_D.csv', 'r') as readFrom:
    reader=csv.reader(readFrom.readlines())
with open("EUR_USD_D_DATA.csv", 'w', newline='') as writeTo:
    writer=csv.writer(writeTo)
    for line in reader:
        #first few vaules cant have an EMA since we need more data points
        #along with EMA calculation
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

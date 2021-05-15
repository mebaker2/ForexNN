import sys
import requests
import time
import datetime
import csv

currentEpoch=int(time.time())
baseEpoch=1199224800
hourly=11088600
halfHour=int(hourly/2)
fiftenMin=int(hourly/4)
fiveMin=int(hourly/12)
nextEpoch=1199224800+fiveMin
#11088600

filename=str("SPX500_USD_5M.csv")
with open(filename, 'w', newline='') as file:
    writer=csv.writer(file)
    writer.writerow(["Date","Open","High","Low","Close","Volume","Pips","Percent"])
    linesWrote=0
    apiCalls=0
    while 1:
        if nextEpoch > currentEpoch:
            break
        r = requests.get('https://finnhub.io/api/v1/forex/candle?symbol=OANDA:SPX500_USD&resolution=5&from='+str(baseEpoch)+'&to='+str(nextEpoch)+'&token=c2evmaaad3i9kmvt4ci0')
        apiCalls+=1
        if r.status_code==200:
            if r.json()['s']!='ok':
                continue
            c=r.json()['c']
            h=r.json()['h']
            l=r.json()['l']
            o=r.json()['o']
            t=r.json()['t']
            v=r.json()['v']
            count=0
            for bobSaget in c:
                pips=round( ((float(c[count])-float(o[count]))*10000),2 )
                percent=round((round(float(c[count])-float(o[count]),5)/float(o[count]))*100.0,4)
                englishDate= time.strftime("%d %b %Y %H:%M", time.localtime(t[count]))
                writer.writerow([englishDate,o[count],h[count],l[count],c[count],v[count],pips,percent])
                linesWrote+=1
                count+=1
        baseEpoch=nextEpoch
        nextEpoch+=fiveMin
        print("Written up to epoch:"+str(baseEpoch))
        print("Written Lines:"+str(linesWrote))
        print("API calls:"+str(apiCalls))
        time.sleep(1)

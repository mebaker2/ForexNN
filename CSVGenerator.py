import sys
import requests
import time
import csv

#some time epochs that i constantly used while changing the candle rate
currentEpoch=int(time.time())
baseEpoch=1199224800
hourly=11088600
halfHour=int(hourly/2)
fiftenMin=int(hourly/4)
fiveMin=int(hourly/12)

#epoch step up used for the api calls
nextEpoch=1199224800+fiveMin
filename=str("SPX500_USD_5M.csv")
with open(filename, 'w', newline='') as file:
    writer=csv.writer(file)
    writer.writerow(["Date","Open","High","Low","Close","Volume","Pips","Percent"])
    #mostly used for tracking progress in the printlines at the bottom
    linesWrote=0
    apiCalls=0
    while 1:
        #quick way to make sure i dont make an invalid request
        if nextEpoch > currentEpoch:
            break
        #api call replace the token feild with your own key from finnhub
        r = requests.get('https://finnhub.io/api/v1/forex/candle?symbol=OANDA:SPX500_USD&resolution=5&from='+str(baseEpoch)+'&to='+str(nextEpoch)+'&token=XXXX')
        apiCalls+=1
        #making sure the call worked
        if r.status_code==200:
            if r.json()['s']!='ok':
                continue
            #parsing
            c=r.json()['c']
            h=r.json()['h']
            l=r.json()['l']
            o=r.json()['o']
            t=r.json()['t']
            v=r.json()['v']
            count=0
            for bobSaget in c:
                #write the data and do a little bitmath for additional data
                pips=round( ((float(c[count])-float(o[count]))*10000),2 )
                percent=round((round(float(c[count])-float(o[count]),5)/float(o[count]))*100.0,4)
                englishDate= time.strftime("%d %b %Y %H:%M", time.localtime(t[count]))
                writer.writerow([englishDate,o[count],h[count],l[count],c[count],v[count],pips,percent])
                linesWrote+=1
                count+=1
        #epoch step up and data print out to track progress
        baseEpoch=nextEpoch
        nextEpoch+=fiveMin
        print("Written up to epoch:"+str(baseEpoch))
        print("Written Lines:"+str(linesWrote))
        print("API calls:"+str(apiCalls))
        time.sleep(1)

#coding:utf-8

import requests
import json
import time

url = "http://v.ubox.cn/win/ajax_winner_pars/"

#i['userId'],i['nickname'],i['openId'],i['vmcode'],i['pid'],i['pname'],i['price'],i['payAmount'],i['payTime'],i['transactionId']

#print "userid","nickname","openid","vmcode","pid","pname","price","payamount","time","transid"
#for i in js:
#    print i['userId'],i['nickname'],i['pname'],i['treadNo'],i['price'],i['payAmount'],i['payTime'],i['transactionId'],i['openId']

success = 0
fail = 0
filename = str(time.localtime().tm_mon)+'_'+str(time.localtime().tm_mday)+'.csv'
f = open(filename,'w')
res = requests.get(url)
last = json.loads(res.content.decode('utf-8'))
for k in range(0,100000):
    res = requests.get(url)
    js = json.loads(res.content.decode('utf-8'))
    if last == js:
        time.sleep(1)
        continue
    for i in js:
        t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(i['payTime']))
        a = ",%s,%s,%s,%s,%s,%s\n"%(i['payTime'],i['transactionId'],i['treadNo'],i['transactionId'][-10:],i['price'],int(i['transactionId'])%int(i['price']))
        #print t,a
        print(a)
        f.write(t+a)
    last = js
    time.sleep(1)
    k += 1
f.close()

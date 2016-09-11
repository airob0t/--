#coding:utf-8

import requests
import json

url = "http://buy.ubox.cn/machine/search.html? "
r = requests.session()
r.headers['User-Agent'] = "Android"
r.headers['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
f = open('uboxvm.txt','w')
for i in range(0,1000000):
    data = "key="+str(i)+"&page=1"
    res = r.post(url,data=data)
    js = json.loads(res.content)
    if js['data'] != [] and js['data']['list'] != []:
        a = js['data']['list'][0]
        #print i,a[u'address'],a[u'provinces'],a[u'name'],a[u'typeName'],a[u'areaName']
        t = "%d,%s,%s,%s,%s,%s\n" % (i,a[u'address'],a[u'provinces'],a[u'name'],a[u'typeName'],a[u'areaName'])
        print t.encode('utf-8').strip()
        f.write(t.encode('utf-8'))

f.close()

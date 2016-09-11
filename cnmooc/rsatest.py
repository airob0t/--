#coding:utf-8

import rsa
import binascii
import requests

url = "http://www.cnmooc.org/home/login.mooc"
loginurl = "http://www.cnmooc.org/home/doLogin.mooc"
username = "kangxizhen@qq.com".replace('@',"%40")    #用户名
pwd = "123qwe" #密码

def encrypt(plaintext_text):
    plaintext = int(plaintext_text.encode('hex'), 16)
    ciphertext = pow(plaintext, exponent,modulus)
    return '%X' % ciphertext

r = requests.session()
r.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
res = r.get(url)
start = res.content.find("tokenId")+16
end = res.content.find('"',start)
token = res.content[start:end]+'\n'+pwd
#print token
modulus = "0088d263588e5916662b39e30319cc92f995f8a5555458830cac272e8d9d12328ff3fa023a4c0bee12248264c1dc46165a37c617b217cfaf3d010f941bafd89dc035ac81b58c5ca7eb9027d7bca9ae33805ed77b9af79338b2c824ba1c5fde7d1010c6024ebaa1a1cf164323ce46fdf8d64ad6f207ca156c204b454c8a1bb8325b"
exponent = "010001"
modulus = int(modulus,16)
exponent = int(exponent,16)
strtoken = encrypt(token[::-1]).lower()
#print strtoken
r.headers['X-Requested-With'] = "XMLHttpRequest"
r.headers['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
r.headers['Referer'] = "http://www.cnmooc.org/home/login.mooc"
data = "loginName="+username+"&strToken="+strtoken+"&loginType=0&isCheckCode=0&historyUrl=&lang=zh_CN"
res = r.post(loginurl,data=data)
print res.content


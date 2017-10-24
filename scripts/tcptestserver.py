#coding:utf-8

from socket import *

s = socket()
#host = gethostname()
host = '0.0.0.0'
port = 137
s.bind((host,port))

s.listen(5)
while True:
    c, addr = s.accept()
    print u'连接地址:',addr
    command = c.recv(1024)
    print command
    if command == 'close':
        c.close()
        break
s.close()

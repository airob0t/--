#coding:utf-8

import socket

s = socket.socket()
#host = socket.gethostname()
host = '' #ip
port = 12365  #port
try:
    s.connect((host, port))
    s.send(raw_input())
    s.close()
    print 'sended'
except:
    print 'connect failed,check ip or port'
raw_input()

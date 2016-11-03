#coding:utf-8

from socket import *
from tkinter import *

s = socket()
host = gethostname()
port = 12345
s.bind((host,port))

def display(name):
    root = Tk()
    root.mainloop()

s.listen(5)
while True:
    c, addr = s.accept()
    print u'连接地址:',addr
    command = s.recv(1024)
    try:
        start_new_thread(display,(command))
    except:
        print 'start new thread failed'
    c.close()
c.close()

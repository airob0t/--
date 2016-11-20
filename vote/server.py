#coding:utf-8

from socket import *
from tkinter import *
from thread import *


s = socket()
host = gethostname()
port = 12357
s.bind((host,port))
global root

def display(command):
    global root
    root = Tk()
    root.geometry('640x480')
    root.mainloop()


s.listen(5)
while True:
    c, addr = s.accept()
    print u'连接地址:',addr
    command = c.recv(1024)
    print command
    if command == 'close':
        root.quit()
        c.close()
        continue
    elif command == 'exit':
        c.close()
        break
    try:
        start_new_thread(display,(command,))
        print command
    except:
        print 'start new thread failed'
    c.close()
s.close()

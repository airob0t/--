#coding=utf-8
from Tkinter import *
from socket import *
import time
import threading
import tkMessageBox
import sys


class myApp:
    def __init__(self,master):
        self.show = True
        self.update = False
        self.str = 'AIRobot'
        self.frame = Frame(master)
        self.frame.pack()
        self.l = Label(self.frame,text="AIRobot", bg='green',font=("Arial", 72),width=15, height=4)
        self.l.grid(row=1,column=0,columnspan=2, sticky=W+E+N+S)
        self.root = master
        self.loop()
    
    def loop(self):
        if self.show:
            self.root.deiconify()
        else:
            self.root.iconify()
            self.root.attributes('-topmost', 1)
        if self.update:
            self.update = False
            self.l['text'] = self.str
        self.root.after(100,self.loop)

class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.root = Tk()
        self.app = myApp(self.root)
        self.root.mainloop()

    def hide(self):
        self.app.show = False
    def show(self):
        self.app.show = True
    def setext(self,txt):
        self.app.str = txt
        self.app.update = True

if __name__ =='__main__':
    s = socket()
    #host = gethostname()
    host = '' #ip
    port = 12365  #port
    try:
        s.bind((host,port))
        s.listen(15)
        print 'listen',port
    except:
        print 'cannot listen',port
        raw_input()
        sys.exit(0)
    th = myThread()
    th.start()
    while True:
        c, addr = s.accept()
        print u'连接地址:',addr
        command = c.recv(1024)
        print command
        if command == 'hide':
            th.hide()
        elif command != '':
            th.setext(command.decode('gbk'))
            th.show()
        elif command == 'exit':
            s.close()
            break

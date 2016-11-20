#coding=utf-8
from Tkinter import *
from socket import *
import time
import threading
import tkMessageBox

exitFlag = showFlag = False

class App:
  def __init__(self,master):
    frame = Frame(master)
    frame.pack()
    self.button1 = Button(frame,text = 'start',fg='red',command=self.start_hi)
    self.button1.pack(side=LEFT)
    self.button2 = Button(frame,text='stop',fg = 'blue',command=self.say_stop)
    self.button2.pack(side=LEFT)
    self.root=master
    #self.update_clock()
    

  def start_hi(self):
    self.thread = myThread()
    self.thread.start()
    self.update_clock()

  def say_stop(self):
    global exitFlag
    global showFlag
    exitFlag = True
    
  def update_clock(self):
    global exitFlag
    global showFlag
    if exitFlag:
      print 'exit'
      return
    if showFlag:
      print 'show'
      showFlag = False
      tkMessageBox.showinfo('show', 'Hello World')
    self.root.after(100, self.update_clock)

class myThread (threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.s = socket()
    self.host = gethostname()
    self.port = 12360
    self.s.bind((self.host,self.port))
    self.s.listen(5)

  def __del__(self):
    self.s.close()
  
  def run(self):
    global exitFlag
    global showFlag
    while True:
      self.c, self.addr = self.s.accept()
      if exitFlag:
        return
      print u'连接地址:',self.addr
      self.command = self.c.recv(1024)
      print self.command
      if self.command == 'close':
        self.c.close()
      elif self.command == 'exit':
        exitFlag = True
      elif self.command != '':
        showFlag = True
    

#th = myThread()
#th.start()

root = Tk()
app = App(root)
root.mainloop()

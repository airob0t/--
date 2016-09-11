#coding:utf-8

import time as ti

f = open('data.csv','r')
time = []
transid = []
for i in f.readlines():
    time.append(int(i[20:30]))
    transid.append(int(i[31:41]))
sum = 0
i = 0
while i < len(transid):
    sum += transid[i]
    i += 1
avr = sum/len(transid)
i = 0
while i < len(transid):
    if transid[i]<= avr:
        print time[i],ti.strftime('%Y-%m-%d %H:%M:%S',ti.localtime(time[i])),transid[i]%400
    i +=1
f.close()

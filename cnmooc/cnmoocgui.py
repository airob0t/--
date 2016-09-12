#coding:utf-8
from Tkinter import *
import requests
import json

def encrypt(plaintext_text,exponent,modulus):
    plaintext = int(plaintext_text.encode('hex'), 16)
    ciphertext = pow(plaintext, exponent,modulus)
    return '%X' % ciphertext

def login():
    username = text1.get().replace('@',"%40")
    pwd = text2.get()
    examid = text3.get()
    #print username,pwd,examid
    r = requests.session()
    r.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    res = r.get('http://www.cnmooc.org/home/login.mooc')
    start = res.content.find("tokenId")+16
    end = res.content.find('"',start)
    token = res.content[start:end]+'\n'+pwd
    #print token
    modulus = "0088d263588e5916662b39e30319cc92f995f8a5555458830cac272e8d9d12328ff3fa023a4c0bee12248264c1dc46165a37c617b217cfaf3d010f941bafd89dc035ac81b58c5ca7eb9027d7bca9ae33805ed77b9af79338b2c824ba1c5fde7d1010c6024ebaa1a1cf164323ce46fdf8d64ad6f207ca156c204b454c8a1bb8325b"
    exponent = "010001"
    modulus = int(modulus,16)
    exponent = int(exponent,16)
    strtoken = encrypt(token[::-1], exponent, modulus).lower()
    #print strtoken
    r.headers['X-Requested-With'] = "XMLHttpRequest"
    r.headers['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
    r.headers['Referer'] = "http://www.cnmooc.org/home/login.mooc"
    data = "loginName="+username+"&strToken="+strtoken+"&loginType=0&isCheckCode=0&historyUrl=&lang=zh_CN"
    res = r.post('http://www.cnmooc.org/home/doLogin.mooc',data=data)
    #print res.content
    res = r.get('http://www.cnmooc.org/examTest/stuExamList/'+examid+'.mooc')
    htmllist = res.content
    strat = 0
    end = 0
    allans = []
    while True:
        start = htmllist.find('td4" id="',end)
        if start == -1:
            break
        itemstart = htmllist.find('itemId="',start)
        itemend = htmllist.find('"', itemstart+8)
        itemid = htmllist[itemstart+8:itemend]
        end = htmllist.find('"', start+9)
        subid = htmllist[start+9:end]
        #print subid,itemid
        res = r.post('http://www.cnmooc.org/examSubmit/'+examid+'/enterObjectiveExam-'+subid+'.mooc?itemId='+itemid)
        html = res.content
        newstart = html.find('var paperId = \'')
        newend = html.find('\'',newstart+15)
        paperid = html[newstart+15:newend]
        newstart = html.find('var examQuizNum = \'')
        newend = html.find('\'',newstart+19)
        quiznum = html[newstart+19:newend]
        newstart = html.find('var curSubmitNum = \'')
        newend = html.find('\'',newstart+20)
        cursubmitnum = html[newstart+20:newend]
        data = {
            'testPaperId': subid,
            'paperId': paperid,
            'limitTime': '-60',
            'modelType': 'practice',
            'examQuizNum': quiznum,
            'curSubmitNum': cursubmitnum
            }
        #print data
        #res = r.post('http://www.cnmooc.org/examSubmit/'+examid+'/doObjectiveExam-'+subid+'.mooc')
        res = r.post('http://www.cnmooc.org/examSubmit/'+examid+'/getExamPaper-.mooc',data=data)
        #print res.content
        answers = []
        txt = json.loads(res.content)['paper']['paperStruct']   #list
        '''
        a = txt['paper']['paperStruct'][0]['quiz']  #dict
        b = txt['paper']['paperStruct'][1]['quiz']
        a = a['quizOptionses']  #list
        b = b['quizOptionses']
        '''
        #print txt
        for i in range(0,len(txt)):
            answer = ''
            #print "quizId:",txt[i]['quizId'],"quizContent:",txt[i]['quiz']['quizContent']
            option = txt[i]['quiz']['quizOptionses']
            ans = txt[i]['quiz']['quizResponses']
            if len(option)==0 or len(ans)==0:
                #print '\n\noption data error\n'
                break
            for j in option:
                letter = chr(j[u'optionId']-option[0][u'optionId']+ord('A'))
                #print letter,"optionId:",j[u'optionId'],"optionContent:",j[u'optionContent'],"quizId:",j[u'quizId']
            #print "answer:"
            for j in ans:
                letter = chr(j[u'optionId']-option[0][u'optionId']+ord('A'))
                answer += letter
                #print letter,"optionId:",j[u'optionId'],"responseId:",j[u'responseId'],"quizId:",j[u'quizId']
            answers.append(answer)
            #print '\n'
        allans.append(answers)
        #print '本节答案:',answers
        #raw_input('pause')
    #print '全部答案'
    for i in allans:
        for j in i:
            showbox.insert(END,j+' ')
        showbox.insert(END,'\n')

root = Tk()
root.title('CNMOOC客观题答案获取工具 --by AIRobot')
root.geometry('600x480')                 #是x 不是*
root.resizable(width=False, height=True) #宽不可变, 高可变,默认为True
text1 = StringVar()
text2 = StringVar()
text3 = StringVar()
label1 = Label(root,text='账号')
label2 = Label(root,text='密码')
label3 = Label(root,text='examid')
entry1 = Entry(root, textvariable = text1)
entry2 = Entry(root, textvariable = text2, show = '*')
entry3 = Entry(root, textvariable = text3)
showbox = Text(root)
label1.pack()
entry1.pack()
label2.pack()
entry2.pack()
label3.pack()
entry3.pack()
Button(root, text="获取", command = login).pack()
showbox.pack()



root.mainloop()

#coding:utf-8

import requests
import json

url = "http://www.cnmooc.org/examSubmit/2055/getExamPaper-.mooc"
cookie = "moocvk=1f2b44d042d846a9a0f799b19174c60e; objectExamCookie_365566=365566; JSESSIONID=B845386045A40D164DD554CC77EF2310.host-1-1; moocsk=11235f6bf9114430bc16828b9c2d66ae; Hm_lvt_ed399044071fc36c6b711fa9d81c2d1c=1462337781,1462601492,1463190949,1463838875; Hm_lpvt_ed399044071fc36c6b711fa9d81c2d1c=1463838949; BEC=38E7F41348B23C71575CC063D73B304E|V0BpN|V0Bol"
data = "testPaperId=12057&paperId=2830&limitTime=3600&modelType=practice&examQuizNum=25&curSubmitNum=1"

r = requests.session()
r.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
r.headers['Cookie'] = cookie
r.headers['Host'] = "www.cnmooc.org"
r.headers['Accept'] = "application/json, text/javascript, */*; q=0.01"
r.headers['Origin'] = "http://www.cnmooc.org"
r.headers['X-Requested-With'] = "XMLHttpRequest"
r.headers['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"

res = r.post(url,data=data)
txt = json.loads(res.content)['paper']['paperStruct']   #list
'''
a = txt['paper']['paperStruct'][0]['quiz']  #dict
b = txt['paper']['paperStruct'][1]['quiz']
a = a['quizOptionses']  #list
b = b['quizOptionses']
'''
for i in range(0,len(txt)):
    print "quizId:",txt[i]['quizId'],"quizContent:",txt[i]['quiz']['quizContent']
    option = txt[i]['quiz']['quizOptionses']
    ans = txt[i]['quiz']['quizResponses']
    for j in option:
        letter = chr(j[u'optionId']-option[0][u'optionId']+ord('A'))
        print letter,"optionId:",j[u'optionId'],"optionContent:",j[u'optionContent'],"quizId:",j[u'quizId']
    print "answer:"
    for j in ans:
        letter = chr(j[u'optionId']-option[0][u'optionId']+ord('A'))
        print letter,"optionId:",j[u'optionId'],"responseId:",j[u'responseId'],"quizId:",j[u'quizId']
    print '\n'

#coding: utf-8
#import uuid
#import sys
import base64
import json
import requests
import os

asr_server = 'http://tsn.baidu.com/text2audio'
client_id = 'cL3GTL1jHXWNwmVeIyD4Vyzl'
client_secret = 'a46bfd71b4bbfb959b1be5f9c37006dd'
baidu_oauth_url = 'https://openapi.baidu.com/oauth/2.0/token/'+'?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
ans = requests.get(baidu_oauth_url).content
access_token = eval(ans)['access_token']
#mac_address=uuid.UUID(int=uuid.getnode()).hex[-12:]

# utf-8, <1024 byte
def baidu_asr(tex): 
	ans = requests.get(asr_server+'?tex='+tex+'&lan=zh&cuid=112233445566&ctp=1&tok='+access_token)
	audio = open('./put.mp3','wb')
	audio.write(ans.content)

def Answer(content):
	ans = requests.get(u"http://www.tuling123.com/openapi/api?key=8801e702ba740038f11375b205f7882f&userid=78551&info={0}".format(content))
	#print ans.json()['code']
	#print type(ans.json()['code'])
	if ans.json()['code'] == 100000:
		#print ans.json()['code']
		return ans.json()['text']
	elif ans.json()['code'] == 200000:
		#print ans.json()['code']
		return ans.json()['text']+ans.json()['url']
	elif ans.json()['code'] == 302000:
		#print ans.json()['code']
		res = ""
		for list in ans.json()[u'list']:
			res = res +'\n' + list[u'article']+ ' ' +list[u'source']+ ' ' +list[u'detailurl']+'\n'
		return ans.json()[u'text']+'\n'+res
	elif ans.json()['code'] == 305000:
		#print ans.json()['code']
		res = ""
		for list in ans.json()[u'list']:
			res = res + '\n' +list[u'trainnum']+ ' ' +list[u'start']+ ' ' +list[u'terminal']+ ' ' +list[u'starttime']+ ' ' +list[u'endtime']+'\n' +list[u'detailurl']+'\n'
		return ans.json()[u'text']+'\n'+res
	elif ans.json()['code'] == 306000:
		#print ans.json()['code']
		res = ""
		for list in ans.json()[u'list']:
			res = res +'\n' + list[u'flight']+ ' ' +list[u'route']+ ' ' +list[u'startime']+ ' ' +list[u'endtime']+ ' ' +list[u'state']+ ' ' +list[u'detailurl']+'\n'
		return ans.json()[u'text']+'\n'+res
	elif ans.json()['code'] == 308000:
		res = ""
		for list in ans.json()[u'list']:
			res = res +'\n' + list[u'name']+ ' ' +list[u'info']+ ' ' +list[u'detailurl']+'\n'
		return ans.json()[u'text']+'\n'+res

print "************************************"
print "************************************"


while True:
	print "我说:".decode('utf-8'),
	text = raw_input()
	text = Answer(text.decode('gbk'))
	print 'AIRobot:'+text
	if len(text)>=1024:
		print "The length of tex out of range."
		baidu_asr('回答内容过长，超出限制范围')
		os.system('lame --decode put.mp3 put.wav &>/dev/null')
		os.system('python wav.py')
	else :
                baidu_asr(text)
		os.system('lame --decode put.mp3 put.wav &>/dev/null')
		os.system('python wav.py')



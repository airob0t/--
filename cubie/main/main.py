# -*- coding: utf-8 -*-
import subprocess
import SUNXI_GPIO as GPIO
import time
import base64
import string
import json
import requests
import sys

vtt_server = 'http://vop.baidu.com/server_api'
tts_server = 'http://tsn.baidu.com/text2audio'
client_id = 'cL3GTL1jHXWNwmVeIyD4Vyzl'
client_secret = 'a46bfd71b4bbfb959b1be5f9c37006dd'
baidu_oauth_url = 'https://openapi.baidu.com/oauth/2.0/token/'+'?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
#print baidu_oauth_url
ans = requests.get(baidu_oauth_url).content
access_token = eval(ans)['access_token']

def baidu_asr(speech_file):
	with open(speech_file, 'rb') as f:
		speech_data = f.read()
	speech_base64=base64.b64encode(speech_data).decode('utf-8')
	speech_length=len(speech_data)
	data_dict = {'format':'wav', 'rate':16000, 'channel':1, 'cuid':'112233445566', 'token':access_token, 'lan':'zh', 'speech':speech_base64, 'len':speech_length}
	json_data = json.dumps(data_dict).encode('utf-8')
	json_length = len(json_data)
	headers = {
				'Content-Type': 'application/json',
				'Content-Length': json_length
				}
	fs = requests.post(vtt_server,headers=headers,data=json_data)
	result_str = fs.content.decode('utf-8')
	json_resp = json.loads(result_str)
	return json_resp

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

def tts(tex):
	ans = requests.get(tts_server+'?tex='+tex+'&lan=zh&cuid=112233445566&ctp=1&tok='+access_token)
	audio = open('./tmp.mp3','wb')
	audio.write(ans.content)

GPIO.init()
BUTTON = GPIO.PD2
LED = GPIO.PD1
GPIO.setcfg(BUTTON, GPIO.IN)
GPIO.setcfg(LED, GPIO.OUT)

r = 0
print "Ready"
while True:
	state = GPIO.input(BUTTON)
	if state == GPIO.HIGH and r == 0 :
		child = subprocess.Popen("arecord -D \"plughw:1,0\" -r 16000 -c 1 -f S16_LE ./tmp.wav",shell=True)
		r = 1
	elif state == GPIO.LOW and r == 1 :
		print child.pid
		time.sleep(0.2)
		subprocess.call("kill "+str(child.pid+1), shell=True)
		r = 0
		#subprocess.call("python wav.py ./tmp.wav",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		rs = baidu_asr('./tmp.wav')
		#print type(rs[u'err_no'])
		if rs[u'err_no'] == 0:
			vtt = ''.join(rs[u'result'])
			if u'开灯' in vtt:
				GPIO.output(LED, GPIO.HIGH)
				print "turn on the light"
				tts("灯已打开")
				subprocess.call("lame --decode tmp.mp3 tmp.wav &>/dev/null", shell=True)
				subprocess.call("python wav.py ./tmp.wav",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				subprocess.call("rm tmp.mp3 tmp.wav",shell=True)
				continue
			elif u'关灯' in vtt:
				GPIO.output(LED, GPIO.LOW)
				print "turn off the light"
				tts("灯已关闭")
				subprocess.call("lame --decode tmp.mp3 tmp.wav &>/dev/null", shell=True)
				subprocess.call("python wav.py ./tmp.wav",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				subprocess.call("rm tmp.mp3 tmp.wav",shell=True)
				continue
			elif u'播放音乐' in vtt:
				print "play music"
				child = subprocess.Popen("python wav.py ./cmusic/test.wav",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				while True :
					if GPIO.input(BUTTON) == GPIO.HIGH:
						subprocess.call("kill "+str(child.pid+1), shell=True)
						break
				time.sleep(0.2)
				continue
			elif u'语音记事本' in vtt:
				tts("语音记事按下按钮后开始")
				subprocess.call("lame --decode tmp.mp3 tmp.wav &>/dev/null", shell=True)
				subprocess.call("python wav.py ./tmp.wav",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				subprocess.call("rm tmp.mp3 tmp.wav",shell=True)
				while True :
					if GPIO.input(BUTTON) == GPIO.HIGH:
						child = subprocess.Popen("arecord -D \"plughw:1,0\" -r 16000 -c 1 -f S16_LE ./crecord/tmp.wav",shell=True)
						while GPIO.input(BUTTON) == GPIO.HIGH:
							pass
						time.sleep(0.2)
						subprocess.call("kill "+str(child.pid+1), shell=True)
						tts("语音记事结束")
						subprocess.call("lame --decode tmp.mp3 tmp.wav &>/dev/null", shell=True)
						subprocess.call("python wav.py ./tmp.wav",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
						subprocess.call("rm tmp.mp3 tmp.wav",shell=True)
						break
				continue
			else :
				result = Answer(vtt)
				tts(result)
		else :
			tts("识别失败")
		subprocess.call("lame --decode tmp.mp3 tmp.wav &>/dev/null", shell=True)
		subprocess.call("python wav.py ./tmp.wav",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		subprocess.call("rm tmp.mp3 tmp.wav",shell=True)
		#exit()


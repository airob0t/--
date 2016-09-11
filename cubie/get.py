import base64
import json
import requests
import sys

asr_server = 'http://vop.baidu.com/server_api'
client_id = 'cL3GTL1jHXWNwmVeIyD4Vyzl'
client_secret = 'a46bfd71b4bbfb959b1be5f9c37006dd'
baidu_oauth_url = 'https://openapi.baidu.com/oauth/2.0/token/'+'?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
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
	fs = requests.post(asr_server,headers=headers,data=json_data)
	result_str = fs.content.decode('utf-8')
	json_resp = json.loads(result_str)
	return json_resp

r = baidu_asr('./get.wav')
print r[u'result']


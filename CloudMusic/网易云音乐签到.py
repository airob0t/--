#coding:utf-8
import requests,json,os,base64,re
from Crypto.Cipher import AES
import hashlib,time


username = ''
password = ''


modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
           'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
           '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
           '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
           '3ece0462db0a22b8e7')
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'
default_timeout = 2
	
def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext

def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text.encode('hex'), 16)**int(pubKey, 16)%int(modulus, 16)
    return format(rs, 'x').zfill(256)

def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]

def encrypted_request(text):
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {
        'params': encText,
        'encSecKey': encSecKey
        }
    return data

class signin(object):
    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36',  # NOQA
            'Cookie': 'appver=1.5.2;'
        }
        self.session = requests.Session()
        self.music_u = ''

    def login(self, username, password):
        pattern = re.compile(r'^0\d{2,3}\d{7,8}$|^1[34578]\d{9}$')
        if (pattern.match(username)):
            return self.phone_login(username, password)
        action = 'https://music.163.com/weapi/login/'
        text = {
            'username': username,
            'password': hashlib.md5(password.encode()).hexdigest(),
            'rememberLogin': 'true'
        }
        data = encrypted_request(text)
        try:
            res = self.session.post(action, headers=self.header, data=data)
            self.music_u = res.cookies.get('MUSIC_U')
            return json.loads(res.content)
        except requests.exceptions.RequestException as e:
            return {'code': 501}

    def phone_login(self, username, password):
        action = 'https://music.163.com/weapi/login/cellphone'
        text = {
            'phone': username,
            'password': hashlib.md5(password.encode()).hexdigest(),
            'rememberLogin': 'true'
        }
        data = encrypted_request(text)
        try:
            res = self.session.post(action, headers=self.header, data=data)
            self.music_u = res.cookies.get('MUSIC_U')
            return json.loads(res.content)
        except requests.exceptions.RequestException as e:
            return {'code': 501}

    def daily_signin(self, web=True, android=True):
        REQUEST_URL = 'http://music.163.com/api/point/dailyTask?csrf_token=placeholder&type={}'
        TYPE_WEB = 1
        TYPE_ANDROID = 0
        """签到

        usage:

            >>> from nesign import nesign
            >>> result = nesign('MY MUSIC_U')
            {'android': {'point': 3, 'code': 200}, 'web': {'point': 2, 'code': 200}}
            >>> result = nesign('MY MUSIC_U') # 错误一般会有一个 msg 字段
            {'android': {'code': -2, 'msg': '重复签到'}, 'web': {'code': -2, 'msg': '重复签到'}}
            >>> result = nesign('一个非法的 MUSIC_U') # 当然也有特例
            {'android': {'code': 301}, 'web': {'code': 301}}

        :type music_u: str
        :param music_u: 你的登陆 token，可以在 web 端下登录后在 music.163.com 域下的 cookies 找到
        :param web: web 端两经验签到
        :param android: android 端三点经验签到

        :rtype: dict
        """
        cookies = {'MUSIC_U': self.music_u}
        headers = {'Referer': 'http://music.163.com/'}
        result = {}
        if not (web or android):
            raise ValueError('至少指定一种签到类型')
        if web:
            url = REQUEST_URL.format(TYPE_WEB)
            response = requests.post(url, cookies=cookies, headers=headers)
            result['web'] = response.json()
        if android:
            url = REQUEST_URL.format(TYPE_ANDROID)
            response = requests.post(url, cookies=cookies, headers=headers)
            result['android'] = response.json()
        return result

sign = signin()

while True:
    current_time = time.localtime()
    if current_time.tm_hour == 1:
        sign.login(username, password)
        print sign.daily_signin()
    time.sleep(3600)



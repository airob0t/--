#coding:utf-8
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from qiangda.settings import STATIC_ROOT
from models import *

def init(request):
    Person.objects.get_or_create(code=1,name='#')
    Status.objects.get_or_create(code=1,stat=-1)
    return HttpResponse('OK')

def get(request):
    tag = Status.objects.filter(code=1)[0].stat
    if tag == -1:
        name = Person.objects.filter(code=1)[0].name
        return HttpResponse(name)
    else:
        return HttpResponse('#')

def index(request):
    #Person.objects.get_or_create(code=1,name='#')
    #Status.objects.get_or_create(code=1,stat=-1)
    a = request.GET.get('id',None)
    m1 = '<script>alert("抢答还没有开始！")</script>'
    tag = Status.objects.filter(code=1)[0].stat
    if a is None:
        html = '''
<!DOCTYPE html>
<meta charset="utf-8">
<html>
<body>
<form action="/" method="get">
请输入姓名：<input type=text name="id" value="" /><br />
<input type="submit" value="进入抢答页面">
</form>
</body>
</html>'''
    elif tag==0:
        html = '''
    <!DOCTYPE html>
    <meta charset="utf-8">
    <html>
    <body>
    <form action="/" method="get">
    <input type=hidden name="id" value="'''+a.encode('utf-8')+'''" />
    <input type="submit" value="点 击 抢 答" style="height: 500px; width: 500px; border-color: #F00; font-size: 36px; background-color: #0F0;" />
    </form> '''+m1+'''
    </body>
    </html>'''
    elif tag == 1:
        obj = Status.objects.filter(code=1)[0]
        obj.stat = -1
        obj.save()
        obj = Person.objects.filter(code=1)[0]
        obj.name = request.GET.get('id').encode('utf-8')
        obj.save()
        html = '''
<!DOCTYPE html>
<meta charset="utf-8">
<html>
<body>
<form action="/" method="get">
<input type=hidden name="id" value="'''+a.encode('utf-8')+'''">
<input type="submit" value="点 击 抢 答" style="height: 500px; width: 500px; border-color: #F00; font-size: 36px; background-color: #0F0;" />
</form> <script>alert("抢答成功！")</script>
</body>
</html>'''
        return HttpResponse(html)
    elif tag == -1:
        no = Person.objects.filter(code=1)[0].name
        html = '''
<!DOCTYPE html>
<meta charset="utf-8">
<html>
<body>
<form action="/" method="get">
<input type=hidden name="id" value="'''+a.encode('utf-8')+'''">
<input type="submit" value="点 击 抢 答" style="height: 500px; width: 500px; border-color: #F00; font-size: 36px; background-color: #0F0;" />
</form> <script>alert("已有人抢答！抢答者:'''+no.encode('utf-8')+'''")</script>
</body>
</html>'''
    return HttpResponse(html)

def send(request):
    a = request.GET.get('tag',None)
    no = Person.objects.filter(code=1)[0].name
    if a is None:
        html = '''<!DOCTYPE html>
<meta charset="utf-8">
<html>
<body>
<form action="/send/" method="get">
<input type=hidden name="tag" value="0">
<input type="submit" value="关闭抢答" style="height: 50px; width: 100px;" />
</form><br />
<form action="/send/" method="get">
<input type=hidden name="tag" value="1">
<input type="submit" value="开启抢答" style="height: 50px; width: 100px;" />
</form><br />
<a href="/send/">刷新</a><br />
当前抢答者：'''+no.encode('utf-8')+'''
</body>
</html>'''
        return HttpResponse(html)
    else:
        while True:
            try:
                f = open(STATIC_ROOT+'tag.txt','w')
            except:
                continue
            break
        obj = Status.objects.filter(code=1)[0]
        obj.stat = request.GET['tag']
        obj.save()
        html = '''<!DOCTYPE html>
<meta charset="utf-8">
<html>
<body>
<form action="/send/" method="get">
<input type=hidden name="tag" value="0">
<input type="submit" value="关闭抢答" style="height: 50px; width: 100px;" />
</form><br />
<form action="/send/" method="get">
<input type=hidden name="tag" value="1">
<input type="submit" value="开启抢答" style="height: 50px; width: 100px;" />
</form><br /><script>alert("修改成功")</script>
<a href="/send/">刷新</a><br />
当前抢答者：'''+no.encode('utf-8')+'''
</body>
</html>'''
        return HttpResponse(html)


#coding:utf-8
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from qiangda.settings import STATIC_ROOT

def index(request):
    a = request.GET.get('id',None)
    m1 = '<script>alert("抢答还没有开始！")</script>'
    while True:
        try:
            f = open(STATIC_ROOT+'tag.txt','r')
        except:
            continue
        break
    tag = int(f.read())
    f.close()
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
        while True:
            try:
                f = open(STATIC_ROOT+'tag.txt','w')
            except:
                continue
            break
        f.write("-1")
        f.close()
        while True:
            try:
                f = open(STATIC_ROOT+'no.txt','w')
            except:
                continue
            break
        f.write(request.GET.get('id').encode('utf-8'))
        f.close()
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
        while True:
            try:
                f = open(STATIC_ROOT+'no.txt','r')
            except:
                continue
            break
        no = f.read()
        f.close()
        html = '''
<!DOCTYPE html>
<meta charset="utf-8">
<html>
<body>
<form action="/" method="get">
<input type=hidden name="id" value="'''+a.encode('utf-8')+'''">
<input type="submit" value="点 击 抢 答" style="height: 500px; width: 500px; border-color: #F00; font-size: 36px; background-color: #0F0;" />
</form> <script>alert("已有人抢答！抢答者:'''+no+'''")</script>
</body>
</html>'''
    return HttpResponse(html)

def send(request):
    a = request.GET.get('tag',None)
    while True:
        try:
            f = open(STATIC_ROOT+'no.txt','r')
        except:
            continue
        break
    no = f.read()
    f.close()
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
当前抢答者：'''+no+'''
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
        f.write(request.GET['tag'])
        f.close()
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
当前抢答者：'''+no+'''
</body>
</html>'''
        return HttpResponse(html)


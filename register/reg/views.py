from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from models import Person


def index(request):
    if request.method == 'GET':
		return render(request,'reg.html',{'js':''})
    if 'stuid' not in request.POST or 'stuname' not in request.POST:
        return render(request,'reg.html',{'js':'<script>alert(\'Please input the correct info!\');</script>'})
    stuid = request.POST['stuid']
    stuname = request.POST['stuname']
    if not stuid.isdigit() or len(stuid) != 10 or len(stuname)>10:
        return render(request,'reg.html',{'js':'<script>alert(\'length error,please input the real info!\');</script>'})
    p = Person(name=stuname, stuid=stuid)
    p.save()
    return render(request,'reg.html',{'js':'<script>alert(\'OK!\');</script>'})

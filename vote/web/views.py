#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from web.models import Person,IP
# Create your views here.

def index(request):
    person = Person.objects.all()
    return render(request,'index.html',{'person':person})

def vote(request):
    if 'name' not in request.GET:
        return HttpResponse(u'非法操作')
    person = Person.objects.get(name=request.GET['name'])
    if person.isOpen != True:
        return HttpResponse(u'投票已关闭')
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    try:
        t = IP.objects.get(ip=ip)
        return HttpResponse(u'已经投过票')
    except IP.DoesNotExist:
        person.ticket += 1
        person.save()
        IP.objects.create(ip=ip)
        return HttpResponse(u'投票成功')
    return HttpResponse(u'500')

def admin(request):
    stat = request.GET.get('open','-1')
    if stat =='0' or stat =='1' and 'name' in request.GET :
        person = Person.objects.get(name=request.GET['name'])
        if stat == '0':
            person.isOpen = False
        else:
            person.isOpen = True
        person.save()
        return HttpResponse(u'操作成功')
    person = Person.objects.all()
    return render(request,'admin.html',{'person':person})


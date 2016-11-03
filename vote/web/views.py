#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from web.models import Person
# Create your views here.

def index(request):
    person = Person.objects.all()
    return render(request,'index.html',{'person':person})

def vote(request):
    if 'name' not in request.GET:
        return HttpResponse(u'非法操作')
    person = Person.objects.filter(name=request.GET['name'])[0]
    if person.isOpen != True:
        return HttpResponse(u'投票已关闭')
    person.ticket += 1
    person.save()
    return HttpResponse(u'投票成功')

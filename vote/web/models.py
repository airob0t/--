from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Person(models.Model):
    #stuid = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    ticket = models.IntegerField(default=0)
    isOpen = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s %d' %(self.name,self.ticket)

class IP(models.Model):
    ip = models.GenericIPAddressField()
    
    def __unicode__(self):
        return '%s' %(self.ip)

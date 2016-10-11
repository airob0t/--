from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Person(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=100)

    def __unicode__(self):  # __str__ on Python 3
        return self.name

class Status(models.Model):
    code = models.IntegerField()
    stat = models.IntegerField(default=0)

    def __unicode__(self):  # __str__ on Python 3
        return self.name

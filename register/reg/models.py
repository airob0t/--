from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Person(models.Model):
    stuid = models.CharField(max_length=10)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name+self.stuid

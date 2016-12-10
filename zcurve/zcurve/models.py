from __future__ import unicode_literals

from django.db import models

# Create your models here.
class result(models.Model):
    inname = models.CharField(max_length=50)
    outname = models.CharField(max_length=50)

    def __unicode__(self):
        return self.inname+':'+self.outname
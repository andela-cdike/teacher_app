from __future__ import unicode_literals

from django.db import models


class Base(models.Model):
    '''Common fields'''
    name = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Class(Base):
    '''Represents Teacher's classes'''
    teacher = models.ForeignKey(
        'authentication.Teacher', related_name='classes'
    )

    def __unicode__(self):
        return self.name

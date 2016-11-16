from __future__ import unicode_literals

from django.db import models
from django.urls import reverse


class Base(models.Model):
    '''Common fields'''
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Class(Base):
    '''Represents Teacher's classes'''
    name = models.CharField(max_length=50, unique=True)
    teacher = models.ForeignKey(
        'authentication.Teacher', related_name='classes'
    )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('class-detail', kwargs={'pk': self.id})


class Student(Base):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, default='')
    my_class = models.ForeignKey(
        'Class', related_name='students'
    )

    def __unicode__(self):
        return '{0} {1} {2}'.format(
            self.first_name,
            self.middle_name,
            self.last_name
        )


class Subject(Base):
    title = models.CharField(max_length=50, unique=True)
    students = models.ManyToManyField(Student)

    def __unicode__(self):
        return self.title

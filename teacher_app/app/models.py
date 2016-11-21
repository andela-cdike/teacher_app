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
    total = models.IntegerField(null=True)
    average = models.FloatField(null=True)

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
    age = models.IntegerField()
    total = models.IntegerField(null=True)
    average = models.FloatField(null=True)

    def __unicode__(self):
        return '{0} {1} {2}'.format(
            self.first_name,
            self.middle_name,
            self.last_name
        )

    def save(self, *args, **kwargs):
        super(Student, self).save(*args, **kwargs)
        class_total = Student.objects.filter(
            my_class=self.my_class.pk).aggregate(
            models.Sum('total'))['total__sum']
        if class_total:
            self.my_class.total = class_total
            count = ScoreSheet.objects.filter(
                student__my_class=self.my_class.pk).count()
            self.my_class.average = self.my_class.total / float(count)
            self.my_class.save()


class Subject(Base):
    title = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.title


class ScoreSheet(Base):
    student = models.ForeignKey('Student', related_name='score')
    subject = models.ForeignKey('Subject')
    score = models.IntegerField(null=True)

    class Meta:
        unique_together = ('subject', 'student')

    def __unicode__(self):
        return '{0} scored {1} in {2}'.format(
            str(self.student),
            self.score,
            self.subject.title
        )

    def save(self, *args, **kwargs):
        super(ScoreSheet, self).save(*args, **kwargs)
        score_sum = ScoreSheet.objects.filter(
            student=self.student.pk
        ).aggregate(models.Sum('score'))['score__sum']
        if score_sum:
            self.student.total = score_sum
            count = ScoreSheet.objects.filter(
                student=self.student.pk).count()
            self.student.average = score_sum / float(count)
            self.student.save()

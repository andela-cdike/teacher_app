from django import forms

from app.models import Class, Student


class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = ('name',)


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'middle_name')

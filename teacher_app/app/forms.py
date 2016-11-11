from django import forms

from app.models import Class


class ClassCreateForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = ('name',)

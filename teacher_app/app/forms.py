from django import forms

from app.models import Class, ScoreSheet, Student, Subject


class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = ('name',)


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'middle_name', 'age')

    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all().order_by('title'), required=False
    )

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        student = kwargs.get('instance', None)
        if student:
            self.fields['subjects'].initial = [
                s.pk for s in ScoreSheet.objects.filter(student=student.id)
            ]


class ScoreSheetForm(forms.ModelForm):

    class Meta:
        model = ScoreSheet
        fields = ('student', 'subject', 'score')

    def __init__(self, *args, **kwargs):
        super(ScoreSheetForm, self).__init__(*args, **kwargs)
        score_sheet = kwargs.get('instance', None)
        if score_sheet:
            self.fields['student'].initial = score_sheet.student
            self.fields['subject'].inital = score_sheet.subject

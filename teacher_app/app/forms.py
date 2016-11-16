from django import forms

from app.models import Class, Student, Subject


class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = ('name',)


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'middle_name')

    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), required=False
    )

    # Overriding save allows us to process the value of 'subjects' field
    def save(self, commit=True):
        # Get the unsave Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the student with subjects
            instance.subject_set.clear()
            for subject in self.cleaned_data['subjects']:
                instance.subject_set.add(subject)
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance

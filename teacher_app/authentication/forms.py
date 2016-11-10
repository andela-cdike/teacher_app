from django.contrib.auth.forms import UserCreationForm

from authentication.models import Teacher


class RegisterForm(UserCreationForm):

    class Meta:
        model = Teacher
        fields = (
            'first_name', 'last_name', 'username', 'password1', 'password2'
        )

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from forms import TeacherRegisterForm
from models import Teacher


class TeacherRegisterView(SuccessMessageMixin, CreateView):
    '''Handles User Signup
        Raw data posted from form is received here, bound to form
    as dictionary and sent to unrendered dango form for validation.

    Returns: A HTTP Response with a register template, otherwise,
             redirects to the login page.
    '''
    model = Teacher
    form_class = TeacherRegisterForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        '''Activate Teacher if form is valid'''
        self.object = form.save(commit=False)
        self.object.active = True
        super(TeacherRegisterView, self).form_valid(form)

    def form_invalid(self, form):
        '''Add error messages to the messages framework'''
        for key in form.errors:
            for error in form.errors[key]:
                messages.add_message(self.request, messages.ERROR, error)
        return super(TeacherRegisterView, self).form_invalid(form)

    def get_success_message(self, cleaned_data):
        success_message = (
            "You have successfully signed up. Login to gain access to app."
        )
        return success_message

    def get_context_data(self, *args, **kwargs):
        '''Add title to context'''
        context = super(TeacherRegisterView,
                        self).get_context_data(*args, **kwargs)
        context['title'] = 'Register'
        return context

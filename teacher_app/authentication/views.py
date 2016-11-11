from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from forms import RegisterForm
from models import Teacher


class RegisterView(SuccessMessageMixin, CreateView):
    '''Handles User Signup'''
    model = Teacher
    form_class = RegisterForm
    template_name = 'authentication/authentication.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        '''Activate Teacher if form is valid'''
        self.object = form.save(commit=False)
        self.object.active = True
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        '''Add error messages to the messages framework'''
        for key in form.errors:
            for error in form.errors[key]:
                messages.add_message(self.request, messages.ERROR, error)
        return super(RegisterView, self).form_invalid(form)

    def get_success_message(self, cleaned_data):
        success_message = (
            "You have been successfully registered. "
            "Login to gain access to app."
        )
        return success_message

    def get_context_data(self, *args, **kwargs):
        '''Add title to context'''
        context = super(RegisterView,
                        self).get_context_data(*args, **kwargs)
        context['title'] = 'register'
        return context


class LoginView(FormView):
    '''Handles User Login'''
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'authentication/authentication.html'

    def form_valid(self, form):
        '''Logs user in if form validation passes'''
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        '''Add error messages to the messages framework'''
        for key in form.errors:
            for error in form.errors[key]:
                messages.add_message(self.request, messages.ERROR, error)
        return super(LoginView, self).form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        '''Add title to context'''
        context = super(LoginView,
                        self).get_context_data(*args, **kwargs)
        context['title'] = 'login'
        return context

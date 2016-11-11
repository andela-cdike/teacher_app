from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from authentication.models import Teacher
from forms import ClassCreateForm
from models import Class, Student


class IndexView(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'app/index.html'
    context_object_name = 'classes'

    def get_queryset(self):
        '''Return only classes owned by current user'''
        queryset = super(IndexView, self).get_queryset()
        queryset = queryset.filter(teacher=self.request.user)
        return queryset


class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Class
    template_name = 'app/create-class.html'
    success_url = reverse_lazy('index')
    form_class = ClassCreateForm

    def form_valid(self, form):
        '''Make current user the teacher of this class'''
        self.object = form.save(commit=False)
        teacher = Teacher.objects.get(pk=self.request.user.pk)
        self.object.teacher = teacher
        return super(ClassCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        '''Add title to context'''
        context = super(
            ClassCreateView, self).get_context_data(**kwargs)
        context['title'] = 'create new class'
        context['url_name'] = 'create-class'
        return context


class ClassDetailView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'app/class-detail.html'
    context_object_name = 'students'

    def get_queryset(self):
        '''Return only students that belong to the calling class'''
        queryset = super(ClassDetailView, self).get_queryset()
        queryset = queryset.filter(my_class=self.kwargs['pk'])
        return queryset

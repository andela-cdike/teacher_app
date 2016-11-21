from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from authentication.models import Teacher
from forms import ClassForm, ScoreSheetForm, StudentForm
from models import Class, ScoreSheet, Student, Subject


class IndexView(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'app/index.html'
    context_object_name = 'classes'

    def get_queryset(self):
        '''Return only classes owned by current user'''
        currently_ranked_by = self.request.GET.get('ranked_by', 'name')
        queryset = super(IndexView, self).get_queryset()
        queryset = queryset.filter(teacher=self.request.user).order_by(
            currently_ranked_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            IndexView, self).get_context_data(**kwargs)
        context['currently_ranked_by'] = self.request.GET.get('ranked_by',
                                                              'name')
        return context


class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Class
    template_name = 'app/create-class.html'
    success_url = reverse_lazy('index')
    form_class = ClassForm

    def form_valid(self, form):
        '''Make current user the teacher of this class'''
        self.object = form.save(commit=False)
        teacher = Teacher.objects.get(pk=self.request.user.pk)
        self.object.teacher = teacher
        return super(ClassCreateView, self).form_valid(form)

    def form_invalid(self, form):
        '''Add error messages to the messages framework'''
        for key in form.errors:
            for error in form.errors[key]:
                messages.add_message(self.request, messages.ERROR, error)
        return super(ClassCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(
            ClassCreateView, self).get_context_data(**kwargs)
        context['title'] = 'create new class'
        context['url_name'] = 'create-class'
        return context


class ClassUpdateView(LoginRequiredMixin, UpdateView):
    model = Class
    context_object_name = 'class'
    template_name = 'app/edit-class.html'
    form_class = ClassForm
    success_url = reverse_lazy('index')

    def form_invalid(self, form):
        '''Add error messages to the messages framework'''
        for key in form.errors:
            for error in form.errors[key]:
                messages.add_message(self.request, messages.ERROR, error)
        return super(ClassUpdateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(
            ClassUpdateView, self).get_context_data(**kwargs)
        context['url_name'] = 'edit-class'
        context['title'] = 'edit class'
        return context


class ClassDetailView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'app/class-detail.html'
    context_object_name = 'students'

    def get_queryset(self):
        '''Return only students that belong to the calling class'''
        filter_id = int(self.request.GET.get('filter', 0))

        # if filtering based on students offering particular subject
        if filter_id:
            subject = Subject.objects.get(pk=filter_id)
            queryset = Student.objects.filter(score__subject=subject)
        else:
            queryset = super(ClassDetailView, self).get_queryset()
            queryset = queryset.filter(my_class=self.kwargs['pk'])
            query_string = self.request.GET.get('q', None)
            # deal with non-age based queries
            age_based_queryset = queryset.filter(pk=-1)
            if query_string:
                name_based_queryset = queryset.filter(
                    Q(first_name__icontains=query_string) |
                    Q(last_name__icontains=query_string) |
                    Q(middle_name__icontains=query_string)
                )
                if query_string.isdigit():
                    age_based_queryset = queryset.filter(
                        age__exact=int(query_string)
                    )
                queryset = name_based_queryset | age_based_queryset
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            ClassDetailView, self).get_context_data(**kwargs)
        my_class = Class.objects.get(pk=self.kwargs['pk'])
        subjects = Subject.objects.all()
        context['class'] = my_class
        context['subjects'] = subjects
        context['selected_filter'] = int(self.request.GET.get('filter', 0))
        return context


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    template_name = 'app/create-student.html'
    form_class = StudentForm

    def form_valid(self, form):
        '''
        Add relationship between this student, subject and scores
        '''
        self.object = form.save(commit=False)
        students_class = Class.objects.get(pk=self.kwargs['pk'])
        self.object.my_class = students_class
        self.object.save()

        # Add entry in score sheet table
        for subject in form.cleaned_data['subjects']:
            ScoreSheet.objects.create(
                student=self.object, subject=subject)
        return super(StudentCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(
            StudentCreateView, self).get_context_data(**kwargs)
        context['class_id'] = self.kwargs['pk']
        context['title'] = 'Add Student'
        return context

    def get_success_url(self):
        return reverse('class-detail', kwargs={'pk': self.kwargs['pk']})


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    context_object_name = 'student'
    template_name = 'app/edit-student.html'
    form_class = StudentForm

    def form_invalid(self, form):
        '''Add error messages to the messages framework'''
        for key in form.errors:
            for error in form.errors[key]:
                messages.add_message(self.request, messages.ERROR, error)
        return super(StudentUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        '''Update relationship between student, subject and scores'''
        self.object = form.save(commit=False)
        self.object.save()

        # Add entry in score sheet table
        for subject in form.cleaned_data['subjects']:
            ScoreSheet.objects.create(
                student=self.object, subject=subject)
        return super(StudentUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(
            StudentUpdateView, self).get_context_data(**kwargs)
        context['url_name'] = 'edit-student'
        context['title'] = 'edit student'
        return context

    def get_success_url(self):
        return reverse('class-detail', kwargs={'pk': self.kwargs['class_id']})


class StudentDetailView(LoginRequiredMixin, ListView):
    model = ScoreSheet
    template_name = 'app/student-detail.html'
    context_object_name = 'score_sheet'

    def get_queryset(self):
        '''Return only subjects student is taking'''
        queryset = super(StudentDetailView, self).get_queryset()
        queryset = queryset.filter(student=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        student = Student.objects.get(pk=self.kwargs['pk'])
        context['student'] = student
        return context


class AssignScoreView(LoginRequiredMixin, UpdateView):
    model = ScoreSheet
    context_object_name = 'scores'
    template_name = 'app/assign-score.html'
    form_class = ScoreSheetForm

    def form_invalid(self, form):
        '''Add error messages to the messages framework'''
        for key in form.errors:
            for error in form.errors[key]:
                messages.add_message(self.request, messages.ERROR, error)
        return super(AssignScoreView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(
            AssignScoreView, self).get_context_data(**kwargs)
        context['title'] = "assign student's score"
        context['pk'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse(
            'student-detail',
            kwargs={
                'class_id': self.object.student.my_class.pk,
                'pk': self.object.student.pk
            }
        )

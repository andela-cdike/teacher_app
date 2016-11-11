from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from models import Class


class IndexView(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'app/index.html'
    context_object_name = 'classes'

    def get_queryset(self):
        '''Return only classes owned by current user'''
        queryset = super(IndexView, self).get_queryset()
        queryset = queryset.filter(teacher=self.request.user)
        return queryset

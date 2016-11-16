from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create-class/$',
        views.ClassCreateView.as_view(),
        name='create-class'),
    url(r'^class/(?P<pk>[0-9]+)$',
        views.ClassDetailView.as_view(),
        name='class-detail'),
    url(r'^class/(?P<pk>[0-9]+)/edit/$',
        views.ClassUpdateView.as_view(),
        name='edit-class'),

    # Student Views
    url(r'^class/(?P<pk>[0-9]+)/create-student/$',
        views.StudentCreateView.as_view(),
        name='create-student'),
    url(r'^class/(?P<class_id>[0-9]+)/student/(?P<pk>[0-9]+)/edit/$',
        views.StudentUpdateView.as_view(),
        name='edit-student'),
    url(r'^class/(?P<class_id>[0-9]+)/student/(?P<pk>[0-9]+)$',
        views.StudentDetailView.as_view(),
        name='student-detail'),
]

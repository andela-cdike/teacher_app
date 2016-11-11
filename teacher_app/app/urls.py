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
]

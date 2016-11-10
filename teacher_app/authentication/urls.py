from django.conf.urls import url

import views

urlpatterns = [
    url(r'^register', views.TeacherRegisterView.as_view(), name='register'),
]

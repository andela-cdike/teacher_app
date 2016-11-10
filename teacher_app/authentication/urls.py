from django.conf.urls import url

import views

urlpatterns = [
    url(r'^register', views.RegisterView.as_view(), name='register'),
    url(r'^login', views.LoginView.as_view(), name='login'),
]

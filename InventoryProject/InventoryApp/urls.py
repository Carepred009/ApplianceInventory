from django.urls import path

from .views import BaseView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',BaseView.as_view(), name="home"),


path('logout/', auth_views.LogoutView.as_view(), name="logout"),


]
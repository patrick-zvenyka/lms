from .views import *
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('', Login, name='stud-login'),
    path('register', Register, name='stud-register'),
]
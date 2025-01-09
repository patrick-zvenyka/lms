from django.urls import path
from .views import *
urlpatterns = [
    path('', Login, name='lib-login'),
    path('home', Dashboard, name='lib-dashboard'),
]
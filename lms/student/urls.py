from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *
urlpatterns = [
    path('register/', register, name='stud-register'),
    path('', login_view, name='stud-login'),
    path('logout/', LogoutView.as_view(next_page='stud-login'), name='stud-logout'),
    path('dashboard/', Dashboard, name='stud-dashboards'),
]
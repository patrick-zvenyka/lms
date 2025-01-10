from django.urls import path
from .views import *
urlpatterns = [
    path('', Login, name='lib-login'),
    path('librarian/logout/', Logout, name='logout'),
    path('home', Dashboard, name='lib-dashboard'),
    path('books', Books, name='lib-book-list'),
    path('billing', Billing, name='lib-billing'),
]
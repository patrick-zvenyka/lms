from django.urls import path
from .views import *
urlpatterns = [
    path('', Login, name='lib-login'),
    path('librarian/logout/', Logout, name='logout'),
    path('home', Dashboard, name='lib-dashboard'),
    path('books', Books, name='lib-book-list'),
    path('books/history', BookHistory, name='lib-book-view'),
    path('books/new', NewBook, name='lib-new-book'),
    path('borrowing',NewBorrow, name='lib-borrow'),
    path('books/borrowed',BorrowedBooks, name='lib-books-borrowed'),
    path('return-book/<int:borrow_id>/', ReturnBook, name='lib-return-book'),
    path('billing', Billing, name='lib-billing'),
]
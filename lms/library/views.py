from django.shortcuts import render,  redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from base.models import *
from django.db.models import Sum
from django.db.models import Count
from datetime import date
from django.db.models import F, Value, Case, When, BooleanField
# Create your views here.
def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Get username from the input name
        password = request.POST.get("password")  # Get password from the input name
        
        user = authenticate(request, username=username, password=password)  # Authenticate user
        if user is not None:
            if user.groups.filter(name='Librarians').exists():  # Check if the user is in the 'Librarians' group
                login(request, user)
                return redirect('lib-dashboard')  # Redirect to dashboard
            else:
                messages.error(request, "You do not have the required permissions to access this system.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'Librarian/sign-in.html')

def Logout(request):
    logout(request)
    return redirect('lib-login')  

@login_required(login_url='lib-login')
def Dashboard(request):
    total_books = Book.objects.all().count()
    total_users = Student.objects.all().count()
    total_books_borrowed = Borrow.objects.filter(status='borrowed').count()
    total_penalty = Borrow.objects.aggregate(total_fine=Sum('fine'))['total_fine'] or 0

    books = Book.objects.values('subject__name').annotate(subject_count=Count('subject'))
   # Fetch books and their statuses
    books_statuses = Borrow.objects.annotate(
        book_title=F('book__title'),  # Get the book title
        current_status=F('status'),  # Get the borrow status
        book_due_date=F('due_date'),  # Due date for borrowing
        overdue=Case(
            When(due_date__lt=date.today(), then=Value(True)),  # Overdue if due_date < today
            default=Value(False),
            output_field=BooleanField()
        )
    ).values('book_title', 'current_status', 'book_due_date', 'overdue')
    
    context = {
        'title':'Dashboard',
        'total_books':total_books,
        'users':total_users,
        'books_borrowed':total_books_borrowed,
        'penalty':total_penalty,
        'books':books,
        'books_statuses': books_statuses,
    }
    return render(request, 'Librarian/dashboard.html', context)

@login_required(login_url='lib-login')
def NewBorrow(request):

    context = {
        'title':'Borrowing'
    }
    return render(request, 'Librarian/borrow.html', context)

@login_required(login_url='lib-login')
def BorrowedBooks(request):

    record = Borrow.objects.all()
    
    context = {
        'title':'Borrowed Books',
        'borrows': record
    }
    return render(request, 'Librarian/books-borrowed.html', context)

@login_required(login_url='lib-login')
def ReturnBook(request, borrow_id):
    borrow = Borrow.objects.get(id=borrow_id)
    if borrow.status == 'borrowed':
        borrow.status = 'returned'
        borrow.return_date = date.today()
        borrow.save()
        messages.success(request, 'Book has been returned successfully.')
    else:
        messages.error(request, 'This book has already been returned.')

    return redirect('lib-books-borrowed')  # Adjust to your appropriate URL pattern


@login_required(login_url='lib-login')
def Books(request):

    context = {
        'title':'Books'
    }
    return render(request, 'Librarian/books-list.html', context)

@login_required(login_url='li-login')
def BookHistory(request):
    

    context = {
        'title' : 'Book History'
    }
    return render(request, 'Librarian/books-view.html', context)


@login_required(login_url='lib-login')
def NewBook(request):

    context = {
        'title':'New Book'
    }
    return render(request, 'Librarian/books-new.html', context)

@login_required(login_url='lib-login')
def Billing(request):
    
    context = {
        'title' : 'Billing'
    }
    return render(request, 'Librarian/billing.html', context)

@login_required(login_url='lib-login')
def Profile(request):

    context = {
        'title' : 'Profile'
    }
    return render(request, 'profile.html', context)
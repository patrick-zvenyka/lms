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
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
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
def Shelves(request):
    shelves = Shelf.objects.annotate(
        book_count=Count('book'),
        space_left=F('capacity') - Count('book')
    )

    # Set up pagination with 10 items per page
    paginator = Paginator(shelves, 10)  # Show 10 shelves per page
    page_number = request.GET.get('page')  # Get the page number from the URL query parameters
    page_obj = paginator.get_page(page_number)  # Get the page object

    context = {
        'title':'Shelves',
        'shelves':shelves,
        'shelves': page_obj,  # Pass the page object to the template
    }
    return render(request, 'Librarian/shelves.html', context)


@login_required(login_url='lib-login')
def NewShelf(request):
    if request.method == "POST":
        name = request.POST.get("shelf_name")  
        capacity = request.POST.get("shelf_capacity")

        # Validate inputs
        if not name or not capacity:
            messages.error(request, "All fields are required!")
        elif not capacity.isdigit() or int(capacity) <= 0:
            messages.error(request, "Capacity must be a positive number!")
        else:
            # Save the new shelf
            Shelf.objects.create(name=name, capacity=int(capacity))
            messages.success(request, "New shelf added successfully!")
            return redirect('shelves')  # Replace 'shelf-list' with the name of your shelf list URL pattern
       
    context = {
        'title':'New Shelf'
    }
    return render(request, 'Librarian/new-shelf.html', context)


@login_required(login_url='lib-login')
def EditShelf(request, shelf_id):
    # Get the shelf object by ID or raise a 404 if not found
    shelf = get_object_or_404(Shelf, id=shelf_id)
    
    if request.method == "POST":
        name = request.POST.get("shelf_name")
        capacity = request.POST.get("shelf_capacity")
        
        # Validate inputs
        if not name or not capacity:
            messages.error(request, "All fields are required!")
        elif not capacity.isdigit() or int(capacity) <= 0:
            messages.error(request, "Capacity must be a positive number!")
        else:
            # Update the shelf details
            shelf.name = name
            shelf.capacity = int(capacity)
            shelf.save()
            messages.success(request, "Shelf updated successfully!")
            return redirect('shelves')  # Replace 'shelves' with your shelf list URL pattern
    
    context = {
        'title': 'Edit Shelf',
        'shelf': shelf
    }
    return render(request, 'Librarian/edit-shelf.html', context)


@login_required(login_url='lib-login')
def DeleteShelf(request, shelf_id):
    # Get the shelf object by ID or raise a 404 if not found
    shelf = get_object_or_404(Shelf, id=shelf_id)

    # Check if the request method is POST to confirm the deletion
    if request.method == "POST":
        shelf.delete()
        messages.success(request, "Shelf deleted successfully!")
        return redirect('shelves')  # Redirect to the shelves list page

    context = {
        'title': 'Delete Shelf',
        'shelf': shelf
    }
    return render(request, 'Librarian/confirm-delete-shelf.html', context)



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

    books = Book.objects.all().order_by('id')

    for book in books:
        book.is_borrowed = Borrow.objects.filter(book=book, status='borrowed').exists()

    # Set up pagination with 10 items per page
    paginator = Paginator(books, 10)  # Show 10 shelves per page
    page_number = request.GET.get('page')  # Get the page number from the URL query parameters
    page_obj = paginator.get_page(page_number)  # Get the page object

    context = {
        'title':'Books',
        'books':books,
        'books':page_obj
    }
    return render(request, 'Librarian/books-list.html', context)

@login_required(login_url='li-login')
def BookHistory(request, book_id):
    # Get the book object by ID or raise a 404 if not found
    book = get_object_or_404(Book, id=book_id)  # Correct the model to 'Book'
    
    # Check if the book is borrowed
    book.is_borrowed = Borrow.objects.filter(book=book, status='borrowed').exists()

    # Fetch the history of the book (all borrow records)
    book_history = Borrow.objects.filter(book=book).order_by('-borrow_date')  # Adjust based on your model's fields
    
    context = {
        'title': 'Book History',
        'book': book,
        'book_history': book_history  # Pass the borrow history to the template
    }
    
    return render(request, 'Librarian/books-view.html', context)


@login_required(login_url='lib-login')
def NewBook(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        title = request.POST.get('title')
        subject_id = request.POST.get('subject')
        shelf_id = request.POST.get('shelf')
        form = request.POST.get('form')

        # Validate inputs
        if not isbn or not title or not subject_id or not shelf_id or not form:
            messages.error(request, "All fields are required!")
            return redirect('lib-new-book')  # Redirect back to the same page

        try:
            subject = Subject.objects.get(id=subject_id)
            shelf = Shelf.objects.get(id=shelf_id)

            # Check if the shelf is full through the model's save method
            book = Book(isbn=isbn, title=title, subject=subject, shelf=shelf, form=form)
            book.save()  # This will trigger the save method which checks shelf capacity

            messages.success(request, f"Book '{title}' added successfully!")

            return redirect('lib-book-list')  # Redirect to a list of books page (you may adjust this as needed)

        except Shelf.DoesNotExist:
            messages.error(request, "Invalid shelf selected!")
        except Subject.DoesNotExist:
            messages.error(request, "Invalid subject selected!")
        except ValueError as e:
            messages.error(request, str(e))  # Catch and display the error from the save method

    # For GET request, pass shelves and subjects to the context
    shelves = Shelf.objects.all()
    subjects = Subject.objects.all()

    context = {
        'title': 'New Book',
        'shelves': shelves,
        'subjects': subjects,
        'book_form_choices': Book.BOOK_FORM_CHOICES,  # Pass the form choices here
    }
    return render(request, 'Librarian/books-new.html', context)


@login_required(login_url='lib-login')
def EditBook(request, book_id):
    # Fetch the book object by ID or return a 404 error if not found
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        title = request.POST.get('title')
        subject_id = request.POST.get('subject')
        shelf_id = request.POST.get('shelf')
        form = request.POST.get('form')

        # Validate inputs
        if not isbn or not title or not subject_id or not shelf_id or not form:
            messages.error(request, "All fields are required!")
            return redirect('lib-edit-book', book_id=book.id)  # Redirect back to the edit page

        try:
            # Fetch the subject and shelf objects
            subject = Subject.objects.get(id=subject_id)
            shelf = Shelf.objects.get(id=shelf_id)

            # Update the book object with the new values
            book.isbn = isbn
            book.title = title
            book.subject = subject
            book.shelf = shelf
            book.form = form

            # Check if the shelf is full through the model's save method
            book.save()  # This will trigger the save method which checks shelf capacity

            messages.success(request, f"Book '{title}' updated successfully!")

            return redirect('lib-book-list')  # Redirect to the book list page after update

        except Shelf.DoesNotExist:
            messages.error(request, "Invalid shelf selected!")
        except Subject.DoesNotExist:
            messages.error(request, "Invalid subject selected!")
        except ValueError as e:
            messages.error(request, str(e))  # Catch and display the error from the save method

    # For GET request, pass shelves, subjects, and the current book object to the context
    shelves = Shelf.objects.all()
    subjects = Subject.objects.all()

    context = {
        'title': 'Edit Book',
        'shelves': shelves,
        'subjects': subjects,
        'book': book,  # Pass the book object to prepopulate the form
        'book_form_choices': Book.BOOK_FORM_CHOICES,  # Pass the form choices here
    }
    return render(request, 'Librarian/books-edit.html', context)



@login_required(login_url='lib-login')
def DeleteBook(request, book_id):
    # Get the book object by ID or raise a 404 if not found
    book = get_object_or_404(Book, id=book_id)

    # Check if the request method is POST to confirm the deletion
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted successfully!")
        return redirect('lib-book-list')  # Redirect to the books list page

    context = {
        'title': 'Delete Book',
        'book': book
    }
    return render(request, 'Librarian/confirm-delete-book.html', context)





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
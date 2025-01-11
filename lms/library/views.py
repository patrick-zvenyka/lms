from django.shortcuts import render,  redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
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

    context = {
        'title':'Dashboard'
    }
    return render(request, 'Librarian/dashboard.html', context)

@login_required(login_url='lib-login')
def Books(request):

    context = {
        'title':'Books'
    }
    return render(request, 'Librarian/books-list.html', context)

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
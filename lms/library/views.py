from django.shortcuts import render,  redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def Login(request):
    return render(request, 'Librarian/sign-in.html')

def Logout(request):
    logout(request)
    return redirect('lib-login')  

def Dashboard(request):

    context = {
        'title':'Dashboard'
    }
    return render(request, 'Librarian/dashboard.html', context)

def Books(request):

    context = {
        'title':'Books'
    }
    return render(request, 'Librarian/books-list.html', context)


def Billing(request):
    
    context = {
        'title' : 'Billing'
    }
    return render(request, 'Librarian/billing.html', context)

def Profile(request):

    context = {
        'title' : 'Profile'
    }
    return render(request, 'profile.html', context)
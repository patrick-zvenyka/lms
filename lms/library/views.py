from django.shortcuts import render

# Create your views here.
def Login(request):
    return render(request, 'Librarian/sign-in.html')

def Dashboard(request):
    return render(request, 'Librarian/dashboard.html')
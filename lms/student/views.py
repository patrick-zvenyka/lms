from django.shortcuts import render

# Create your views here.
def Login(request):
    return render(request, 'Student/sign-in.html')

def Register(request):
    return render(request, 'Student/sign-up.html')
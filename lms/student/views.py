from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.views import LoginView
# Create your views here.
# Register View
def register(request):
    if request.method == 'POST':
        # Extract data from POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        form = request.POST.get('form')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Construct a form instance with extracted data
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'student_id': student_id,
            'form': form,
            'phone': phone,
            'email': email,
            'password': password
        }
        form = StudentRegistrationForm(data)

        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        # Extract data from POST request
        student_id = request.POST.get('student_id')  # Username equivalent
        password = request.POST.get('password')

        # Construct a form instance with extracted data
        data = {'username': student_id, 'password': password}
        form = CustomLoginForm(data=data)

        if form.is_valid():
            user = authenticate(username=student_id, password=password)
            if user is not None:
                login(request, user)
                return redirect('stud-dashboard')
            else:
                messages.error(request, "Student ID and Password are required!")
                return render('')

        return render( 'stud-login', {'errors': form.errors}, status=400)

    return render(request, 'Student/sign-in.html')



@login_required(login_url='stud-login')
def Dashboard(request):
    
    
    context = {
        'title':'Dashboard',
    }
    return render(request, 'Student/dashboard.html', context)

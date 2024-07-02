from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def BASE(request):
    return render(request,'firstPage.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('employee_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def admin_dashboard(request):
    return render(request, 'admin.html')

@login_required
def employee_dashboard(request):
    return render(request, 'employee.html')


from django.shortcuts import render, redirect
from .forms import RegisterEmployeeForm
from django.contrib.auth import login
from .models import Employee

def register(request):
    if request.method == 'POST':
        form = RegisterEmployeeForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            
            # Extract additional fields from the form and save them to the Employee model
            date_of_joining = form.cleaned_data.get('date_of_joining')
            designation = form.cleaned_data.get('designation')
            contact_no = form.cleaned_data.get('contact_no')
            role = form.cleaned_data.get('role')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            
            Employee.objects.create(
                user=user,
                date_of_joining=date_of_joining,
                designation=designation,
                contact_no=contact_no,
                role=role,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            
            login(request, user)
            return redirect('admin_dashboard' if role == 'ADMIN' else 'employee_dashboard')
    else:
        form = RegisterEmployeeForm()
    return render(request, 'register.html', {'form': form})
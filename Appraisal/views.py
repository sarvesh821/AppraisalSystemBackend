from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect
from .forms import AdminAttributesRatingForm, AdminTaskRatingForm, RegisterEmployeeForm, TaskForm
from django.db.models import Q

from .models import Attributes, Employee, Task,User
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
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def admin_dashboard(request):
    employees_with_tasks = Employee.objects.filter(
        Q(task__is_appraisable=True) & Q(task__rating__isnull=True)
    ).distinct()

    return render(request, 'admin.html', {'employees_with_tasks': employees_with_tasks})

@login_required
def employee_tasks(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    tasks = Task.objects.filter(employee=employee)

    return render(request, 'employee_tasks.html', {'employee': employee, 'tasks': tasks})


# def employee_tasks(request, employee_id):
#     employee = get_object_or_404(Employee, id=employee_id)
#     tasks = Task.objects.filter(employee=employee)
    
#     # Check if all attributes for the employee are null
#     attributes_null = all(getattr(employee.attributes, f'attribute{i}', None) is None for i in range(1, 11))
    
#     context = {
#         'employee': employee,
#         'tasks': tasks,
#         'attributes_null': attributes_null,
#     }
#     return render(request, 'employee_tasks.html', context)
@login_required
def employee_dashboard(request):
    return render(request, 'employee.html')



def register(request):
    if request.method == 'POST':
        form = RegisterEmployeeForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            
           
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



@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.employee = request.user.employee
            task.save()
            return redirect('employee_dashboard')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})
@login_required
@user_passes_test(lambda u: u.is_staff)
def save_rating(request, task_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        task = get_object_or_404(Task, pk=task_id)
        task.rating = rating
        task.save()
        return redirect('admin_dashboard') 
    else:
        return render(request, 'error.html', {'message': 'Method not allowed.'})

@login_required
def rate_employee_attributes(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    attributes, created = Attributes.objects.get_or_create(employee=employee)

    if request.method == 'POST':
        attributes_form = AdminAttributesRatingForm(request.POST, instance=attributes)
        if attributes_form.is_valid():
            attributes_form.save()
            return redirect('admin_dashboard')
    else:
        attributes_form = AdminAttributesRatingForm(instance=attributes)
    
    return render(request, 'rate_attributes.html', {
        'attributes_form': attributes_form,
        'employee': employee
    })
@login_required
def request_appraisal(request):
    employee = request.user.employee
    if employee.has_completed_one_year():
        Task.objects.filter(employee=employee).update(is_appraisable=True)
        
        
        return redirect('employee_dashboard')
    else:
        return render(request, 'error.html', {'message': 'You are not eligible for appraisal yet.'})
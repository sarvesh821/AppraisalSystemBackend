from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from .forms import (
    AdminAttributesRatingForm,
    AdminTaskRatingForm,
    RegisterEmployeeForm,
    TaskForm,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Attributes, Employee, Task, User
from Api.serializers import EmployeeSerializer, TaskSerializer
from rest_framework.authtoken.models import Token
def BASE(request):
    return render(request, "firstPage.html")


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'Login successful', 'is_staff': user.is_staff,'token':token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)




    
   
        
        


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def employee_detail(request):
    employee = Employee.objects.get(user=request.user)
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_tasks(request):
    try:
        employee = request.user.employee
        tasks_to_rate = Task.objects.filter(employee=employee, rating=None)
        rated_tasks = Task.objects.filter(employee=employee).exclude(rating=None)

        tasks_to_rate_serializer = TaskSerializer(tasks_to_rate, many=True)
        rated_tasks_serializer = TaskSerializer(rated_tasks, many=True)

        return Response({
            'tasks_to_rate': tasks_to_rate_serializer.data,
            'rated_tasks': rated_tasks_serializer.data,
        })
    except Task.DoesNotExist:
        return Response({'error': 'Tasks not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
@login_required
def admin_dashboard(request):
    employees_with_tasks = Employee.objects.filter(
        Q(task__is_appraisable=True) & Q(task__rating__isnull=True)
    ).distinct()

    return render(request, "admin.html", {"employees_with_tasks": employees_with_tasks})


@login_required
def employee_dashboard(request):
    employee = request.user.employee
    tasks_without_rating = Task.objects.filter(
        employee=employee, rating__isnull=True
    ).exists()

    context = {
        "employee": employee,
        "tasks_without_rating": tasks_without_rating,
    }
    return render(request, "employee.html", context)


@login_required
def employee_tasks(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    tasks = Task.objects.filter(employee=employee)

    return render(
        request, "employee_tasks.html", {"employee": employee, "tasks": tasks}
    )


def register(request):
    if request.method == "POST":
        form = RegisterEmployeeForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            date_of_joining = form.cleaned_data.get("date_of_joining")
            designation = form.cleaned_data.get("designation")
            contact_no = form.cleaned_data.get("contact_no")
            role = form.cleaned_data.get("role")
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")

            Employee.objects.create(
                user=user,
                date_of_joining=date_of_joining,
                designation=designation,
                contact_no=contact_no,
                role=role,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )

            login(request, user)
            return redirect(
                "admin_dashboard" if role == "ADMIN" else "employee_dashboard"
            )
    else:
        form = RegisterEmployeeForm()
    return render(request, "register.html", {"form": form})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    form = TaskForm(request.data)
    if form.is_valid():
        task = form.save(commit=False)
        task.employee = request.user.employee
        task.save()
        return Response({'message': 'Task created successfully'}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@user_passes_test(lambda u: u.is_staff)
def save_rating(request, task_id):
    if request.method == "POST":
        rating = request.POST.get("rating")
        task = get_object_or_404(Task, pk=task_id)
        task.rating = rating
        task.save()

        employee = task.employee

        if Task.objects.filter(employee=employee, rating__isnull=True).exists():

            return redirect("employee_tasks", employee_id=employee.id)
        else:

            return redirect("admin_dashboard")
    else:
        return render(request, "error.html", {"message": "Method not allowed."})


@login_required
def rate_employee_attributes(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    attributes, created = Attributes.objects.get_or_create(employee=employee)

    if request.method == "POST":
        attributes_form = AdminAttributesRatingForm(request.POST, instance=attributes)
        if attributes_form.is_valid():
            attributes_form.save()

            return redirect("employee_tasks", employee_id=employee_id)
    else:
        attributes_form = AdminAttributesRatingForm(instance=attributes)

    return render(
        request,
        "rate_attributes.html",
        {"attributes_form": attributes_form, "employee": employee},
    )


@login_required
def request_appraisal(request):
    employee = request.user.employee
    if employee.has_completed_one_year():
        Task.objects.filter(employee=employee).update(is_appraisable=True)

        return redirect("employee_dashboard")
    else:
        return render(
            request,
            "error.html",
            {"message": "You are not eligible for appraisal yet."},
        )

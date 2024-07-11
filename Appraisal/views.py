from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
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
from Api.serializers import EmployeeSerializer ,TaskSerializer
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
    print(f"Authenticated user: {request.user}")
    if request.user.is_authenticated:
        print("User is authenticated")
    else:
        print("User is not authenticated")

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
def send_tasks_for_appraisal(request):
    if request.method == "POST":
        employee = request.user.employee  
        tasks = Task.objects.filter(employee=employee, is_appraisable=True)
        
       
        tasks.update(is_appraisable=False)  # Example: Update tasks to mark them as not appraisable
        
        return JsonResponse({'message': 'Tasks sent for appraisal successfully'})
    
    # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    

@api_view(['POST'])
def register_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def current_employees(request):
    employees_count = Employee.objects.count()
    return Response({'count': employees_count})
@api_view(['GET'])
def employees_with_unrated_tasks_count(request):
   
    employees = Employee.objects.filter(Q(task__is_appraisable=True) & Q(task__rating__isnull=True)).distinct()
    count = employees.count()
    return Response({'count': count})
@api_view(['GET'])
def EmployeesWithTasksForRating(request):
   
    employees = Employee.objects.filter(Q(task__is_appraisable=True) & Q(task__rating__isnull=True)).distinct()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_employee_tasks(request, employee_id):
    try:
        tasks = Task.objects.filter(employee__id=employee_id,rating__isnull=True)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)































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

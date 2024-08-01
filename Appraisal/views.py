from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from Appraisal.permissions import IsAdminUser
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
from .models import Attributes, Employee, Notification, Task, User
from Api.serializers import AttributesSerializer, EmployeeSerializer, NotificationSerializer ,TaskSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.http import JsonResponse



# //============================================Base===============================================================
# this function is used to get csrf token and set it in cookies
def get_csrf_token(request):
    token = get_token(request)
    response = JsonResponse({'csrfToken': token})
    response.set_cookie('csrftoken', token)  
    return response



# this function is used to display notifications either on employee/admin navbar
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)



# this function is used to mark notifications as read and delete from notification modal
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notifications_as_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    notifications_to_delete = Notification.objects.filter(user=request.user, is_read=True)
    deleted_count, _ = notifications_to_delete.delete() 
    return Response({'message': f'{deleted_count} notifications marked as read and deleted'})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    user_info = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,   
    }
    return Response(user_info)



# this function is used to validate token and if user is admin 
@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def validate_token_admin(request):
    return Response({'detail': 'Token is valid'}, status=status.HTTP_200_OK)



# this function is used to validate employee and check he is not admin
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_token_employee(request):
    if request.user.is_staff:  
        return Response({'detail': 'Admins are not allowed'}, status=status.HTTP_403_FORBIDDEN)
    return Response({'detail': 'Token is valid'}, status=status.HTTP_200_OK)


# //====================================================Login Functionalities=========================================
# this is login function
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        
        if user.is_superuser or Employee.objects.filter(user=user).exists():
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful', 'is_staff': user.is_staff, 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User is not an employee or superuser'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)



#this is logout function
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.auth:
        request.auth.delete()
    return Response({'status': 'success'}, status=200)



# //===========================================Employee Functionalities=======================================
# this function used to display employee details on employee dashboard
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_detail(request):
    employee = Employee.objects.get(user=request.user)
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)



# this function is used to save the task data send by user in tasks modal
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



# this function is used to update data of particular task in task modal
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, employee=request.user.employee)
    except Task.DoesNotExist:
        return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    if task.task_send:
        return Response({"detail": "Cannot edit tasks that have been sent for appraisal"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


# this function is used to split tasks of employee that are rated/not rated and send as a response to frontend
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
        tasks_to_rate = Task.objects.filter(employee=employee, rating=None )
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
  


# this functions sends the tasks to admin when are send by employee
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_tasks_for_appraisal(request):
    if request.method == "POST":
        employee = request.user.employee
        if employee is None:
            return JsonResponse({'error': 'User has no associated employee profile'}, status=400)
        tasks = Task.objects.filter(employee=employee, is_appraisable=True, rating=None,task_send=False)
        if not tasks.exists():
            return JsonResponse({'error': 'No tasks available for appraisal'}, status=404)
        tasks.update(task_send=True)  
        admin_users = User.objects.filter(is_staff=True)  
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                message=f" {employee.first_name} {employee.last_name} has sent tasks for appraisal."
            )
        return JsonResponse({'message': 'Tasks sent for appraisal successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
  


# this function is used to fetch Attributes of employee from employee modal and display on employee side 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_attributes(request):
    try:
        employee = request.user.employee
        attributes = Attributes.objects.get(employee=employee)
        serializer = AttributesSerializer(attributes)
        return Response(serializer.data)
    except Attributes.DoesNotExist:
        return Response({'error': 'Attributes not found for this employee'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
  

# this is used to send data of tasks that are yet not rated by admin
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unrated_tasks_for_user(request):
    user = request.user
    tasks = Task.objects.filter(employee=user.employee, is_appraisable=True, rating=None, task_send=False)
    serializer = TaskSerializer(tasks, many=True)
    return Response({'tasks': serializer.data})

#    //===================================================Admin Functionalities======================================== 
# this function is used to display count of total employees in modal
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def current_employees(request):
    employees_count = Employee.objects.count()
    return Response({'count': employees_count})


# this function is used to display count of employees who have send there tasks for appraisal
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def employees_with_unrated_tasks_count(request):
    one_year_ago = timezone.now().date() - timedelta(days=365)
    employees = Employee.objects.filter(Q(task__is_appraisable=True) & Q(task__task_send=True) & Q(task__rating__isnull=True) & Q(date_of_joining__lte=one_year_ago)).distinct()
    count = employees.count()
    return Response({'count': count})



# this function is used to register a new employee 
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def register_employee(request):

    user_data = {
        'username': request.data.get('username'),
        'email': request.data.get('email'),
        'password': request.data.get('password')
    }
    
    user = User.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password']
    )
    
    employee_data = {
        'user': user.id,  
        'date_of_joining': request.data.get('dateOfJoining'),
        'designation': request.data.get('designation'),
        'contact_no': request.data.get('contactNo'),
        'role': request.data.get('role'),
        'email': request.data.get('email'),
        'first_name': request.data.get('firstName'),
        'last_name': request.data.get('lastName'),
        'date_of_birth':request.data.get('dateOfBirth'),
        'location':request.data.get('location')
    }
    
    serializer = EmployeeSerializer(data=employee_data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED,)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# this function used to filter employees who have send there tasks for appraisal
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def EmployeesWithTasksForRating(request):
    one_year_ago = timezone.now().date() - timedelta(days=365)
    employees = Employee.objects.filter( Q(task__rating__isnull=True) & Q(task__task_send=True) & Q(date_of_joining__lte=one_year_ago)).distinct()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



# this function gives the tasks of employee which he has send for appraisal
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employee_tasks(request, employee_id):
    try:
        tasks = Task.objects.filter(employee__id=employee_id,rating__isnull=True,is_appraisable=True)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



# this function saves rating of particular task when marked 
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def save_task_rating(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    rating = request.data.get('rating')
    if rating is not None and 0 <= rating <= 10:
        task.rating = rating
        task.save()
        employee = task.employee
        Notification.objects.create(
            user=employee.user,
            message=f'Your task "{task.title}" has been rated.'
        )

        return Response({'message': 'Task rating saved successfully'}, status=status.HTTP_200_OK)
        
    else:
        return Response({'error': 'Invalid rating value'}, status=status.HTTP_400_BAD_REQUEST)
    


# this function saves rating of Attributes
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def save_attribute_ratings(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.get('attributes', [])
    if len(data) != 10:
        return Response({'error': 'Exactly 10 attribute ratings are required'}, status=status.HTTP_400_BAD_REQUEST)

    attributes, created = Attributes.objects.get_or_create(employee=employee)
    attributes.time_management = data[0]
    attributes.communication = data[1]
    attributes.creativity = data[2]
    attributes.respect_of_deadlines = data[3]
    attributes.ability_to_plan = data[4]
    attributes.problem_solving = data[5]
    attributes.passion_to_work = data[6]
    attributes.confidence = data[7]
    attributes.adaptable = data[8]
    attributes.learning_power = data[9]
    attributes.save()

    return Response({'message': 'Attribute ratings saved successfully'}, status=status.HTTP_200_OK)




# this function saves the update info send of employee in employee modal
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def edit_employee_details(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        user = employee.user
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
        
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# this function allow to delete employee
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_employee(request, employee_id):
    if request.method == 'DELETE':
        try:
            employee = get_object_or_404(Employee, pk=employee_id)
            user_id = employee.user.id
            employee.delete()
            return JsonResponse({'message': 'Employee and related User deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



# this function filter the tasks of particular employee that are rated
@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser])
def rated_tasks_of_employee(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        rated_tasks = Task.objects.filter(employee=employee).exclude(rating=None)

        rated_tasks_serializer = TaskSerializer(rated_tasks, many=True)

        return Response({
            'employee_name': f"{employee.first_name} {employee.last_name}",
            'rated_tasks': rated_tasks_serializer.data,
        })
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=404)
    except Task.DoesNotExist:
        return Response({'error': 'Tasks not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    


@api_view(['GET'])
def get_employee_details(request, id):
    try:
        employee = Employee.objects.get(id=id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

















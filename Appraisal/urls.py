from django.urls import path, include
from . import views

urlpatterns = [
      path('api/employee/<int:employee_id>/tasks/', views.get_employee_tasks, name='get_employee_tasks'),
     path('api/employees-with-tasks-for-rating/', views.EmployeesWithTasksForRating, name='employees-with-tasks-for-rating'),
     path('api/current-employees/', views.current_employees, name='current_employees'),
        path('api/unrated-employees/', views.employees_with_unrated_tasks_count, name='employees_with_unrated_tasks_count'),
      path('api/register-employee/', views.register_employee, name='register_employee'),
     path('api/send-tasks-for-appraisal/',views.send_tasks_for_appraisal,name='send_tasks_for_appraisal'),
     path('api/employee-tasks/', views.employee_tasks, name='employee_tasks'),
    path('api/create-task/', views.create_task, name='create_task'),
    path('api/employee-detail/', views.employee_detail, name='employee_detail'),
     path('api/login/', views.login_view, name='login'),
     path('api/logout/', views.logout_view, name='logout'),  
    path("api/", include("Api.urls")),
]

from django.urls import path, include
from . import views

urlpatterns = [
    path('api/users/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('api/employee-attributes/',views.employee_attributes, name='employee-attributes'),
    path('api/mark-notifications-as-read/',views.mark_notifications_as_read,name='mark_notifications_as_read'),
    path('api/notifications/',views.notifications,name='notifications'),
    path('api/csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('api/employee/<int:id>/', views.get_employee_details, name='get_employee_details'),
    path('api/task/<int:task_id>/rate/', views.save_task_rating, name='save_task_rating'),
    path('api/employee/<int:employee_id>/attributes/', views.save_attribute_ratings, name='save_attribute_ratings'),
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

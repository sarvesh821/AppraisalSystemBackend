from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.BASE, name="base"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("employee_dashboard/", views.employee_dashboard, name="employee_dashboard"),
    path("register/", views.register, name="register"),
    path("request-appraisal/", views.request_appraisal, name="request_appraisal"),
    path("create-task/", views.create_task, name="create_task"),
    path("save_rating/<int:task_id>/", views.save_rating, name="save_rating"),
    path(
        "employee_tasks/<int:employee_id>/", views.employee_tasks, name="employee_tasks"
    ),
    path(
        "rate_employee_attributes/<int:employee_id>/",
        views.rate_employee_attributes,
        name="rate_employee_attributes",
    ),
    
    
    
    
    
      path('api/employee-tasks/', views.employee_tasks, name='employee_tasks'),
    path('api/create-task/', views.create_task, name='create_task'),
    path('api/employee-detail/', views.employee_detail, name='employee_detail'),
     path('api/login/', views.login_view, name='login'),
     path('api/logout/', views.logout_view, name='logout'),  
    path("api/", include("Api.urls")),
]

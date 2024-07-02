from django.urls import path
from . import views

urlpatterns = [
    path('', views.BASE, name='base'),
     path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('register/', views.register, name='register'),
]

from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Employee(models.Model):
    ROLE_CHOICES = [
        ('EMPLOYEE', 'Employee'),
        ('ADMIN', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_joining = models.DateField()
    designation = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default='EMPLOYEE')
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class Task(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    description = models.TextField()
    time_taken = models.DurationField()
    is_appraisable = models.BooleanField(default=False)
    rating = models.IntegerField(null=True, blank=True)

class Attribute(models.Model):
    designation = models.CharField(max_length=100)
    attribute_name = models.CharField(max_length=100)

class EmployeeAttribute(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)

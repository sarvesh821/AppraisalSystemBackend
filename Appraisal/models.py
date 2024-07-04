from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, timezone
from django.utils import timezone


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
    def has_completed_one_year(self):
        return timezone.now().date() >= self.date_of_joining + timedelta(days=365)

class Task(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    description = models.TextField()
    time_taken = models.DurationField()
    is_appraisable = models.BooleanField(default=False)
    rating = models.IntegerField(null=True, blank=True)
    

class Attributes(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attribute1 = models.IntegerField(null=True, blank=True)
    attribute2 = models.IntegerField(null=True, blank=True)
    attribute3 = models.IntegerField(null=True, blank=True)
    attribute4 = models.IntegerField(null=True, blank=True)
    attribute5 = models.IntegerField(null=True, blank=True)
    attribute6 = models.IntegerField(null=True, blank=True)
    attribute7 = models.IntegerField(null=True, blank=True)
    attribute8 = models.IntegerField(null=True, blank=True)
    attribute9 = models.IntegerField(null=True, blank=True)
    attribute10 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.employee.user.username

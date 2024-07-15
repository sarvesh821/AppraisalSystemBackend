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
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EMPLOYEE')
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

    def has_completed_one_year(self):
        return timezone.now().date() >= self.date_of_joining + timedelta(days=365)

class Task(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,default='Default Title')
    description = models.TextField()
    time_taken = models.DurationField()
    is_appraisable = models.BooleanField(default=False)
    task_send=models.BooleanField(default=False)
    rating = models.IntegerField(null=True, blank=True)
    

class Attributes(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    time_management = models.IntegerField(null=True, blank=True)
    communication = models.IntegerField(null=True, blank=True)
    creativity = models.IntegerField(null=True, blank=True)
    respect_of_deadlines = models.IntegerField(null=True, blank=True)
    ability_to_plan = models.IntegerField(null=True, blank=True)
    problem_solving = models.IntegerField(null=True, blank=True)
    passion_to_work = models.IntegerField(null=True, blank=True)
    confidence = models.IntegerField(null=True, blank=True)
    adaptable = models.IntegerField(null=True, blank=True)
    learning_power = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.employee.user.username
    def all_attributes_not_none(self):
     
        required_attributes = ['attribute1', 'attribute2', 'attribute3', 'attribute4', 'attribute5',
                               'attribute6', 'attribute7', 'attribute8', 'attribute9', 'attribute10']
        for attr in required_attributes:
            if getattr(self, attr) is not None:
                return False
        return True
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

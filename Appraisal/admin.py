from django.contrib import admin
from .models import Employee, Task, Attribute, EmployeeAttribute

admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Attribute)
admin.site.register(EmployeeAttribute)
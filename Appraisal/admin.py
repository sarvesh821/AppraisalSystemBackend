from django.contrib import admin
from .models import Employee, Task, Attributes

admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Attributes)
# admin.site.register(EmployeeAttribute)
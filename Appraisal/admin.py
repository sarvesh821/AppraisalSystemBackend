from django.contrib import admin
from .models import Employee, Task, Attributes,Notification

admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Attributes)
admin.site.register(Notification)
# admin.site.register(EmployeeAttribute)
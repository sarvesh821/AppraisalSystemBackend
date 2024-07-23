from rest_framework import viewsets
from Appraisal.models import Employee, Task, Attributes
from .serializers import EmployeeSerializer, TaskSerializer, AttributesSerializer
from rest_framework.permissions import IsAuthenticated
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class AttributesViewSet(viewsets.ModelViewSet):
    queryset = Attributes.objects.all()
    serializer_class = AttributesSerializer
    permission_classes = [IsAuthenticated]
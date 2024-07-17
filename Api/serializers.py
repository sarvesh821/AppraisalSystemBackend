from rest_framework import serializers
from django.contrib.auth.models import User
from Appraisal.models import Employee, Task, Attributes,Notification
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EmployeeSerializer(serializers.ModelSerializer):
    has_completed_one_year = serializers.SerializerMethodField()
  

    class Meta:
        model = Employee
        fields = ['id', 'user', 'date_of_joining','date_of_birth','location', 'designation', 'contact_no', 'role', 'email', 'first_name', 'last_name', 'has_completed_one_year']
    
    def get_has_completed_one_year(self, obj):
        return obj.has_completed_one_year()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = '__all__'
        
        
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
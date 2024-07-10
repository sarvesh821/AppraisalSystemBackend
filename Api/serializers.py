from rest_framework import serializers
from Appraisal.models import Employee, Task, Attributes

class EmployeeSerializer(serializers.ModelSerializer):
    has_completed_one_year = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'date_of_joining', 'designation', 'contact_no', 'role', 'email', 'first_name', 'last_name', 'has_completed_one_year']

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
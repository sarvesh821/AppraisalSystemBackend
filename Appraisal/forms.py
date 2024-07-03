from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Attributes, Task

class RegisterEmployeeForm(UserCreationForm):
    ROLE_CHOICES = [
        ('EMPLOYEE', 'Employee'),
        ('ADMIN', 'Admin'),
    ]
    
    date_of_joining = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    designation = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_no = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_joining','designation','contact_no','role','password1')
    
    def __init__(self, *args, **kwargs):
        super(RegisterEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'time_taken', 'is_appraisable']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'time_taken': forms.TextInput(attrs={'class': 'form-control'}),
            'is_appraisable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class AdminTaskRatingForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class AdminAttributesRatingForm(forms.ModelForm):
    class Meta:
        model = Attributes
        fields = [
            'attribute1', 'attribute2', 'attribute3', 'attribute4', 'attribute5',
            'attribute6', 'attribute7', 'attribute8', 'attribute9', 'attribute10'
        ]
        widgets = {
            'attribute1': forms.NumberInput(attrs={'class': 'form-control'}),
            'attribute2': forms.NumberInput(attrs={'class': 'form-control'}),
            'attribute3': forms.NumberInput(attrs={'class': 'form-control'}),
            'attribute4': forms.NumberInput(attrs={'class': 'form-control'}),
            'attribute5': forms.NumberInput(attrs={'class': 'form-control'}),
            'attribute6': forms.NumberInput(attrs={'class': 'form-control'}),
            'attribute7': forms.NumberInput(attrs={'class': 'form-control'}),
            'attribute8': forms.NumberInput(attrs={'class': 'form-control'}),
            'attribute9': forms.NumberInput(attrs={'class': 'form-control'}),
            'attribute10': forms.NumberInput(attrs={'class': 'form-control'}),
        }
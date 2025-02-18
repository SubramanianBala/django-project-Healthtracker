from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'age', 'gender', 'address', 'phone_number', 'email', 'medical_condition']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name', 'required': 'required'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name', 'required': 'required'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select date of birth', 'required': 'required'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter address', 'rows': 2, 'required': 'required'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter phone number', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address', 'required': 'required'}),
            'medical_condition': forms.TextInput(attrs={'placeholder': 'Enter medical condition', 'required': 'required'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\d{10}$', phone_number):
            raise ValidationError("Enter a valid 10-digit mobile number.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        phone_number = cleaned_data.get('phone_number')

        
        patient = getattr(self.instance, 'id', None)
        if patient:
            if Patient.objects.filter(first_name=first_name, last_name=last_name).exclude(id=patient).exists():
                self.add_error('first_name', "A patient with this name already exists.")

            if Patient.objects.filter(phone_number=phone_number).exclude(id=patient).exists():
                self.add_error('phone_number', "This phone number is already registered.")
        else: 
            if Patient.objects.filter(first_name=first_name, last_name=last_name).exists():
                self.add_error('first_name', "A patient with this name already exists.")

            if Patient.objects.filter(phone_number=phone_number).exists():
                self.add_error('phone_number', "This phone number is already registered.")
        
        return cleaned_data

from django import forms
from django.core.exceptions import ValidationError
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'age', 'gender', 
            'address', 'phone_number', 'email', 'medical_condition'
        ]
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
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValidationError("Phone number must be exactly 10 digits.")
        if Patient.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("This phone number already exists. Consider using an alternative.")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Patient.objects.filter(email=email).exists():
            raise ValidationError("This email already exists. Consider using an alternative.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name and last_name:
            if Patient.objects.filter(first_name=first_name, last_name=last_name).exists():
                # Raise a non-field error
                raise ValidationError("A patient with this first and last name already exists.")

        return cleaned_data
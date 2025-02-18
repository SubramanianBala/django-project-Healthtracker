from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True)
    age = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    medical_condition = models.CharField(max_length=100, default="")  
    medical_status = models.CharField(max_length=100, blank=True, null=True)  #
    last_health_check_date = models.DateField(blank=True, null=True) 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
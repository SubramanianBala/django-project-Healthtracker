from django.urls import path
from . import views
from .views import update_patient_status

urlpatterns = [
    path('', views.index, name='index'),
    path('patient/new/', views.create_patient, name='create_patient'),
    path('manage/', views.manage_entities, name='manage_entities'), 
    path('update/patient/<int:pk>/', views.update_patient, name='update_patient'),
    path('delete/patient/<int:pk>/', views.delete_patient, name='delete_patient'),
    path('delete_multiple_patients/', views.delete_multiple_patients, name='delete_multiple_patients'),
    path('update_patient/<int:pk>/', update_patient_status, name='update_patient_status'),
]

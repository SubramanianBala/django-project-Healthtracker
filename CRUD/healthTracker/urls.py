from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manage/', views.manage_entities, name='manage_entities'),
    path('patients/new/', views.create_patient, name='create_patient'), 
    path('update/patient/<int:pk>/', views.update_patient, name='update_patient'),
    path('delete/patient/<int:pk>/', views.delete_patient, name='delete_patient'),
    path('delete_multiple_patients/', views.delete_multiple_patients, name='delete_multiple_patients'),
]
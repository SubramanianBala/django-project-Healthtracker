from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient
from .forms import PatientForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'HealthTracker/index.html')

def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_entities')
    else:
        form = PatientForm()
    return render(request, 'HealthTracker/patient_form.html', {'form': form})

def manage_entities(request):
    patient_list = Patient.objects.all()
    paginator = Paginator(patient_list, 5) 

    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)

    return render(request, 'HealthTracker/manage_entities.html', {'patients': patients})

def update_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('manage_entities')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'HealthTracker/patient_form.html', {'form': form})

def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('manage_entities')  
    return render(request, 'HealthTracker/patient_confirm_delete.html', {'patient': patient})


@csrf_exempt
def delete_multiple_patients(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        Patient.objects.filter(id__in=ids).delete()
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt  
def update_patient_status(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        medical_status = data.get("medical_status")
        last_health_check_date = data.get("last_health_check_date")

        try:
            patient = Patient.objects.get(pk=pk)
            patient.medical_status = medical_status
            patient.last_health_check_date = last_health_check_date
            patient.save()
            return JsonResponse({"status": "success"})
        except Patient.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Patient not found."}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)
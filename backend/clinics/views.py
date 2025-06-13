import csv
from django.http import HttpResponse
from django.shortcuts import render

from .forms import ClinicSelectForm
from .models import Phone
from users.models import Doctor
from services.models import DoctorSpecialityRelation
from clinics.models import Clinic


def clinic_info_view(request):
    form = ClinicSelectForm(request.GET or None)
    clinic = None
    phones = []
    doctors_info = []

    if form.is_valid():
        clinic = form.cleaned_data['clinic']
        phones = Phone.objects.filter(clinic=clinic)
        # Получаем врачей и их специальности
        doctors = Doctor.objects.filter(clinic=clinic)
        for doctor in doctors:
            specialities = DoctorSpecialityRelation.objects.filter(doctor=doctor).select_related('speciality')
            speciality_names = ", ".join([rel.speciality.name for rel in specialities])
            doctors_info.append({
                'name': f"{doctor.last_name} {doctor.first_name} {doctor.middle_name}",
                'specialities': speciality_names
            })

    return render(request, 'clinics/clinic_info.html', {
        'form': form,
        'clinic': clinic,
        'phones': phones,
        'doctors_info': doctors_info
    })


def download_clinic_info(request, clinic_id):
    try:
        clinic = Clinic.objects.get(pk=clinic_id)
    except Clinic.DoesNotExist:
        return HttpResponse("Клиника не найдена", status=404)

    phones = Phone.objects.filter(clinic=clinic)
    doctors = Doctor.objects.filter(clinic=clinic)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="clinic_{clinic_id}_info.csv"'

    writer = csv.writer(response)
    writer.writerow(['Название клиники', 'Адрес', 'Часы работы'])
    writer.writerow([clinic.name, clinic.address, clinic.working_hours])
    writer.writerow([])
    writer.writerow(['Телефоны'])
    for phone in phones:
        writer.writerow([phone.phone_number, phone.note])

    writer.writerow([])
    writer.writerow(['Врачи', 'Специализации'])
    for doctor in doctors:
        specialities = DoctorSpecialityRelation.objects.filter(doctor=doctor).select_related('speciality')
        speciality_names = ", ".join([rel.speciality.name for rel in specialities])
        writer.writerow([f"{doctor.last_name} {doctor.first_name} {doctor.middle_name}", speciality_names])

    return response

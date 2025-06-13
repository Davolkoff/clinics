from django.shortcuts import get_object_or_404
import csv
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ServiceSelectForm
from .models import Service
from users.models import Doctor


def doctors_by_service_view(request):
    form = ServiceSelectForm(request.GET or None)
    selected_service = None
    doctors = []

    if form.is_valid():
        selected_service = form.cleaned_data['service']
        if selected_service:
            # Получаем всех врачей, предоставляющих выбранную услугу
            doctors = Doctor.objects.filter(
                doctorservice__service=selected_service
            ).prefetch_related(
                'clinic',
                'doctorspecialityrelation_set__speciality'
            )

    return render(request, 'services/doctors_by_service.html', {
        'form': form,
        'selected_service': selected_service,
        'doctors': doctors,
    })


def download_doctors_by_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    # Получаем врачей, предоставляющих услугу
    doctors = Doctor.objects.filter(
        doctorservice__service=service
    ).prefetch_related(
        'clinic',
        'doctorspecialityrelation_set__speciality'
    )

    # Создаём CSV файл
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="doctors_for_{service.name}.csv"'

    writer = csv.writer(response)
    writer.writerow(['ФИО врача', 'Клиника', 'Специализации'])

    for doctor in doctors:
        specialities = ', '.join(
            [relation.speciality.name for relation in doctor.doctorspecialityrelation_set.all()]
        )
        writer.writerow([
            f"{doctor.last_name} {doctor.first_name} {doctor.middle_name}",
            doctor.clinic.name,
            specialities,
        ])

    return response

from django.shortcuts import render, redirect, get_object_or_404
import csv
from .forms import AppointmentSelectForm, AppointmentFormForDoctor, AppointmentFormForPatient
from .models import ServiceForAppointment, Payment, Appointment, PaymentType

from medical.models import Diagnosis
from medical.forms import DiagnosisForm
from services.forms import ServiceForm
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect

from django.utils.timezone import now
from django.urls import reverse
from django.db import models
from .tasks import appointment_created


def appointment_info_view(request):
    form = AppointmentSelectForm(request.GET or None, user=request.user)
    appointment = None
    services = []
    diagnoses = []
    payment = None

    if form.is_valid():
        appointment = form.cleaned_data['appointment']
        # Получаем услуги, связанные с приёмом
        services = ServiceForAppointment.objects.filter(appointment=appointment).select_related('service')
        # Получаем диагнозы, связанные с приёмом
        diagnoses = Diagnosis.objects.filter(appointment=appointment).select_related('diagnosis_name')
        # Получаем информацию об оплате
        payment = Payment.objects.filter(appointment=appointment).first()

    # Проверка, что пользователь — это доктор
    if request.user.is_authenticated and hasattr(request.user, 'doctor_profile'):
        # Обработка формы для добавления диагноза
        if request.method == 'POST':
            if 'add_diagnosis' in request.POST:
                diagnosis_form = DiagnosisForm(request.POST)
                if diagnosis_form.is_valid():
                    diagnosis = diagnosis_form.save(commit=False)
                    diagnosis.appointment = appointment
                    diagnosis.save()
                    return redirect('appointment_info')  # Перезагружаем страницу
            # Обработка формы для добавления услуги
            elif 'add_service' in request.POST:
                service_form = ServiceForm(request.POST)
                if service_form.is_valid():
                    service = service_form.save(commit=False)
                    service.appointment = appointment
                    service.save()
                    return redirect('appointment_info')  # Перезагружаем страницу
        else:
            diagnosis_form = DiagnosisForm()
            service_form = ServiceForm()

        return render(request, 'appointments/appointment_info.html', {
            'form': form,
            'appointment': appointment,
            'services': services,
            'diagnoses': diagnoses,
            'payment': payment,
            'diagnosis_form': diagnosis_form,
            'service_form': service_form,
        })

    # Если пользователь не доктор, то показываем только информацию для пациента
    elif request.user.is_authenticated and hasattr(request.user, 'patient_profile'):
        return render(request, 'appointments/appointment_info.html', {
            'form': form,
            'appointment': appointment,
            'services': services,
            'diagnoses': diagnoses,
            'payment': payment,
        })

    # Если пользователь не авторизован, возвращаем на страницу авторизации или ошибку
    return redirect('login')


def download_appointment_info(request, appointment_id):
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        return HttpResponse("Приём не найден", status=404)

    services = ServiceForAppointment.objects.filter(appointment=appointment).select_related('service')
    diagnoses = Diagnosis.objects.filter(appointment=appointment).select_related('diagnosis_name')
    payment = Payment.objects.filter(appointment=appointment).first()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="appointment_{appointment_id}_info.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID приёма', 'Дата', 'Время', 'Врач', 'Пациент'])
    writer.writerow([
        appointment.appointment_id,
        appointment.appointment_date,
        appointment.appointment_time,
        f"{appointment.doctor.last_name} {appointment.doctor.first_name}",
        f"{appointment.patient.user.last_name} {appointment.patient.user.first_name}"
    ])

    writer.writerow([])
    writer.writerow(['Услуги', 'Количество', 'Цена (RUB)'])
    for service in services:
        writer.writerow([service.service.name, service.quantity, service.service.price])

    writer.writerow([])
    writer.writerow(['Диагнозы'])
    for diagnosis in diagnoses:
        writer.writerow([diagnosis.diagnosis_name.name])

    writer.writerow([])
    writer.writerow(['Тип оплаты', 'Дата оплаты'])
    if payment:
        writer.writerow([payment.payment_type.name, payment.payment_date])
    else:
        writer.writerow(['Оплата отсутствует', 'N/A'])

    return response


def appointment_management(request):
    user = request.user
    is_doctor = hasattr(user, 'doctor_profile')
    is_patient = hasattr(user, 'patient_profile')

    if not (is_doctor or is_patient):
        raise HttpResponseForbidden("Access restricted to doctors and patients.")

    # Данные для отображения
    if is_doctor:
        doctor = user.doctor_profile
        appointments = Appointment.objects.filter(doctor=doctor).order_by('appointment_date')
    elif is_patient:
        patient = user.patient_profile
        appointments = Appointment.objects.filter(patient=patient).order_by('appointment_date')

    # Выбор формы добавления записи в зависимости от роли
    add_form = None
    if is_doctor:
        add_form = AppointmentFormForDoctor(request.POST or None, doctor=user.doctor_profile)
    elif is_patient:
        add_form = AppointmentFormForPatient(request.POST or None)

    # Обработка добавления записи
    if request.method == 'POST' and 'add_appointment' in request.POST:
        if add_form.is_valid():
            appointment = add_form.save(commit=False)
            if is_doctor:
                appointment.doctor = doctor
            elif is_patient:
                appointment.patient = user.patient_profile
            appointment.save()
            appointment_created.delay(appointment.appointment_id)
            return redirect('appointment_management')

    # Обработка удаления записи
    if request.method == 'POST' and 'delete_appointment' in request.POST:
        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointment, appointment_id=appointment_id)

        # Проверка прав на удаление
        if (is_patient and appointment.patient == user.patient_profile) or \
           (is_doctor and appointment.doctor == user.doctor_profile):
            appointment.delete()
            return redirect('appointment_management')
        else:
            raise HttpResponseForbidden("У вас нет прав на удаление этого приема.")

    context = {
        'appointments': appointments,
        'add_form': add_form,
        'is_doctor': is_doctor,
        'is_patient': is_patient,
    }
    return render(request, 'appointments/appointment_management.html', context)


def payments_view(request):
    if not hasattr(request.user, 'patient_profile'):
        return HttpResponseForbidden("Эту страницу могут посещать только пациенты")

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        payment_type_id = request.POST.get('payment_type_id')
        payment_date = now().date()

        # Создаем запись об оплате
        Payment.objects.create(
            appointment_id=appointment_id,
            payment_type_id=payment_type_id,
            payment_date=payment_date
        )
        return HttpResponseRedirect(reverse('payments_view'))

    # Логика для вывода данных та же
    payments = Payment.objects.select_related('appointment', 'payment_type').filter(
        appointment__patient=request.user.patient_profile
    )
    payment_types = PaymentType.objects.all()

    unpaid_appointments = Appointment.objects.filter(patient=request.user.patient_profile, payment__isnull=True, )

    unpaid_with_costs = []
    for appointment in unpaid_appointments:
        total_cost = ServiceForAppointment.objects.filter(
            appointment=appointment
        ).aggregate(total_price=models.Sum(models.F('quantity') * models.F('service__price')))['total_price'] or 0
        unpaid_with_costs.append((appointment, total_cost))

    return render(request, 'appointments/payments.html', {
        'payments': payments,
        'payment_types': payment_types,
        'unpaid_appointments': unpaid_with_costs,
    })

from django.contrib.auth import authenticate, login
from .forms import PatientRegistrationForm
import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
import csv
from django.http import HttpResponse, HttpResponseForbidden
from users.forms import DoctorForm, PatientSelectionForm, DoctorSelectForm
from django.contrib.auth.models import User
from services.models import DoctorSpecialityRelation, Service
from appointments.models import Appointment
from users.models import Patient, Doctor
from medical.models import Analysis
from django.contrib.auth import logout


def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def custom_logout_view(request):
    logout(request)
    return redirect('home')



def create_doctor(request):
    # Проверяем, является ли пользователь администратором
    if not request.user.is_staff:
        return HttpResponseForbidden("У вас нет прав для просмотра этой страницы.")

    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            # Создание пользователя
            email = form.cleaned_data['email']
            random_password = generate_random_password()
            user = User.objects.create(
                username=email,
                email=email,
                password=make_password(random_password)
            )

            # Создание объекта Doctor
            doctor = form.save(commit=False)
            doctor.user = user
            doctor.save()

            # Добавление специализаций
            specialities = form.cleaned_data['specialities']
            for speciality in specialities:
                DoctorSpecialityRelation.objects.create(doctor=doctor, speciality=speciality)

            # Сообщение об успехе
            return render(request, 'info_page.html', {"info": f"Врач {doctor.first_name} {doctor.last_name} добавлен! Пароль: {random_password}"})
    else:
        form = DoctorForm()

    return render(request, 'users/create_doctor.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя
            user = form.save()

            # Создаем объект пациента
            Patient.objects.create(
                user=user,
                last_name=form.cleaned_data['last_name'],
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data['middle_name'],
                birth_date=form.cleaned_data['birth_date'],
                policy_number=form.cleaned_data['policy_number'],
                phone_number=form.cleaned_data['phone_number'],
                email=form.cleaned_data['email']
            )

            # Логиним пользователя
            login(request, user)

            # Перенаправляем на главную страницу или другую
            return redirect('home')  # Замените 'home' на нужную страницу
    else:
        form = PatientRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)  # Используем email как username
        if user is not None:
            login(request, user)
            return redirect('home')  # Замените на вашу страницу
        else:
            return render(request, 'users/login.html', {'error': 'Неверный email или пароль'})
    return render(request, 'users/login.html')


def patient_info_view(request):
    selected_patient = None
    appointments = []
    analyses = []

    # Проверяем, является ли пользователь доктором или пациентом
    if hasattr(request.user, 'doctor_profile'):  # Врач
        form = PatientSelectionForm(request.GET or None, user=request.user)
        if form.is_valid():
            selected_patient = form.cleaned_data['patient']
    elif hasattr(request.user, 'patient_profile'):  # Пациент
        selected_patient = request.user.patient_profile  # Пациент выбирает только себя
        form = None  # Убираем форму для пациента
    else:
        return HttpResponseForbidden("У вас нет прав для просмотра этой страницы.")

    # Получение информации
    if selected_patient:
        appointments = Appointment.objects.filter(patient=selected_patient).select_related('doctor')
        analyses = Analysis.objects.filter(patient=selected_patient).select_related('analysis_name')

    context = {
        'form': form,
        'selected_patient': selected_patient,
        'appointments': appointments,
        'analyses': analyses,
    }
    return render(request, 'users/patient_info.html', context)


def download_patient_info(request, patient_id=None):
    # Если пользователь пациент, он может скачать только свою информацию
    if hasattr(request.user, 'patient_profile'):
        patient = request.user.patient_profile
    elif hasattr(request.user, 'doctor_profile') and patient_id:  # Если врач, то выбирает пациента
        patient = get_object_or_404(Patient, pk=patient_id)
    else:
        return HttpResponseForbidden("У вас нет прав для скачивания этой информации.")

    appointments = Appointment.objects.filter(patient=patient)
    analyses = Analysis.objects.filter(patient=patient)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="patient_{patient.patient_id}_info.csv"'

    writer = csv.writer(response)
    writer.writerow(['Дата приёма', 'Доктор', 'Диагнозы', 'Услуги'])
    for appointment in appointments:
        diagnoses = ", ".join([str(d.diagnosis_name) for d in appointment.diagnosis_set.all()])
        services = ", ".join([f"{s.service.name} ({s.quantity})" for s in appointment.serviceforappointment_set.all()])
        writer.writerow([
            appointment.appointment_date,
            str(appointment.doctor),
            diagnoses,
            services,
        ])

    writer.writerow([])
    writer.writerow(['Анализы'])
    writer.writerow(['Название анализа', 'Результат', 'Дата анализа'])
    for analysis in analyses:
        writer.writerow([
            analysis.analysis_name.name,
            analysis.result,
            analysis.analysis_date,
        ])

    return response


def doctor_info_view(request):
    form = DoctorSelectForm(request.GET or None)
    doctor = None
    services = []
    specialities = []
    clinic = None

    if form.is_valid():
        doctor = form.cleaned_data['doctor']
        clinic = doctor.clinic
        # Услуги врача
        services = Service.objects.filter(doctorservice__doctor=doctor)
        # Специальности врача
        specialities = DoctorSpecialityRelation.objects.filter(doctor=doctor).select_related('speciality')

    return render(request, 'users/doctor_info.html', {
        'form': form,
        'doctor': doctor,
        'clinic': clinic,
        'services': services,
        'specialities': specialities
    })


def download_doctor_info(request, doctor_id):
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
    except Doctor.DoesNotExist:
        return HttpResponse("Врач не найден", status=404)

    clinic = doctor.clinic
    services = Service.objects.filter(doctorservice__doctor=doctor)
    specialities = DoctorSpecialityRelation.objects.filter(doctor=doctor).select_related('speciality')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="doctor_{doctor_id}_info.csv"'

    writer = csv.writer(response)
    writer.writerow(['Врач', 'Клиника', 'Специализации'])
    writer.writerow([
        f"{doctor.last_name} {doctor.first_name} {doctor.middle_name}",
        clinic.name if clinic else "N/A",
        ", ".join([spec.speciality.name for spec in specialities])
    ])

    writer.writerow([])
    writer.writerow(['Услуги', 'Цена (RUB)'])
    for service in services:
        writer.writerow([service.name, service.price])

    return response

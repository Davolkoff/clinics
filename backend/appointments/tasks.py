from celery import shared_task
from django.core.mail import send_mail
from .models import Appointment

@shared_task
def appointment_created(appointment_id):
    appointment = Appointment.objects.get(appointment_id=appointment_id)
    subject = f'Запись к врачу № {(appointment_id)}'
    message = f'Здравствуйте, {appointment.patient.first_name},\n\n Ваша запись к врачу прошла успешно.'\
              f'Номер Вашей записи: {appointment.appointment_id}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@clinics.com',
                          [appointment.patient.email])
    return mail_sent

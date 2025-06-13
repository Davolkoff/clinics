from django.db import models
from users.models import Patient, Doctor
from services.models import Service


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True, verbose_name="Код приема")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Пациент")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Врач")
    appointment_date = models.DateField(verbose_name="Дата приема")
    appointment_time = models.TimeField(verbose_name="Время приема")

    def __str__(self):
        return f"Прием {self.appointment_id}"

    class Meta:
        verbose_name = "Прием"
        verbose_name_plural = "Приемы"


class ServiceForAppointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name="Прием")
    quantity = models.IntegerField(verbose_name="Количество")

    class Meta:
        unique_together = ('service', 'appointment')
        verbose_name = "Услуга на прием"
        verbose_name_plural = "Услуги на прием"


class PaymentType(models.Model):
    payment_type_id = models.AutoField(primary_key=True, verbose_name="Код типа оплаты")
    name = models.CharField(max_length=50, verbose_name="Название типа оплаты")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип оплаты"
        verbose_name_plural = "Типы оплаты"


class Payment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, verbose_name="Прием")
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, verbose_name="Тип оплаты")
    payment_date = models.DateField(verbose_name="Дата оплаты")

    def __str__(self):
        return f"Платеж {self.id}"

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

from django.db import models
from django.contrib.auth.models import User
from clinics.models import Clinic


class Patient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        verbose_name="Пользователь"
    )
    patient_id = models.AutoField(primary_key=True, verbose_name="Код пациента")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения")
    policy_number = models.BigIntegerField(verbose_name="Номер полиса")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Электронная почта")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"


class Doctor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name="Пользователь"
    )
    doctor_id = models.AutoField(primary_key=True, verbose_name="Код врача")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, verbose_name="Клиника")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество")
    photo = models.ImageField(
        upload_to='users/doctors/',
        verbose_name='Фотография',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

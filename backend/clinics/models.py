from django.db import models


class Clinic(models.Model):
    clinic_id = models.AutoField(primary_key=True, verbose_name="Код клиники")
    name = models.CharField(max_length=254, verbose_name="Название клиники")
    address = models.CharField(max_length=50, verbose_name="Адрес")
    working_hours = models.CharField(max_length=50, verbose_name="Часы работы")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиника"
        verbose_name_plural = "Клиники"


class Phone(models.Model):
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, verbose_name="Клиника")
    note = models.CharField(max_length=100, verbose_name="Примечание")

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"

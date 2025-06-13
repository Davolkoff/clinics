from django.db import models
from users.models import Doctor


class DoctorSpeciality(models.Model):
    speciality_id = models.AutoField(primary_key=True, verbose_name="Код специальности")
    name = models.CharField(max_length=50, verbose_name="Название специальности")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Специальность врача"
        verbose_name_plural = "Специальности врачей"


class DoctorSpecialityRelation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Врач")
    speciality = models.ForeignKey(DoctorSpeciality, on_delete=models.CASCADE, verbose_name="Специальность")

    class Meta:
        unique_together = ('doctor', 'speciality')
        verbose_name = "Связь врача и специальности"
        verbose_name_plural = "Связи врачей и специальностей"


class Service(models.Model):
    service_id = models.AutoField(primary_key=True, verbose_name="Код услуги")
    name = models.CharField(max_length=50, verbose_name="Название услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class DoctorService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Врач")

    class Meta:
        unique_together = ('service', 'doctor')
        verbose_name = "Услуга врача"
        verbose_name_plural = "Услуги врачей"

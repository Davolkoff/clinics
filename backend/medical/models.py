from django.db import models
from users.models import Patient
from appointments.models import Appointment


class AnalysisName(models.Model):
    analysis_name_id = models.AutoField(primary_key=True, verbose_name="Код названия анализа")
    name = models.CharField(max_length=100, verbose_name="Название анализа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Название анализа"
        verbose_name_plural = "Названия анализов"


class Analysis(models.Model):
    analysis_id = models.AutoField(primary_key=True, verbose_name="Код анализа")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Пациент")
    analysis_name = models.ForeignKey(AnalysisName, on_delete=models.CASCADE, verbose_name="Название анализа")
    result = models.CharField(max_length=500, blank=True, verbose_name="Результат")
    analysis_date = models.DateField(verbose_name="Дата анализа")

    def __str__(self):
        return f"Анализ {self.analysis_id}"

    class Meta:
        verbose_name = "Анализ"
        verbose_name_plural = "Анализы"


class DiagnosisName(models.Model):
    diagnosis_name_id = models.AutoField(primary_key=True, verbose_name="Код названия диагноза")
    name = models.CharField(max_length=50, verbose_name="Название диагноза")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Название диагноза"
        verbose_name_plural = "Названия диагнозов"


class Diagnosis(models.Model):
    diagnosis_id = models.AutoField(primary_key=True, verbose_name="Код диагноза")
    diagnosis_name = models.ForeignKey(DiagnosisName, on_delete=models.CASCADE, verbose_name="Название диагноза")
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name="Прием")

    def __str__(self):
        return f"Диагноз {self.diagnosis_id}"

    class Meta:
        verbose_name = "Диагноз"
        verbose_name_plural = "Диагнозы"

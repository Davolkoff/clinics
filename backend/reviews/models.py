from django.db import models
from users.models import Doctor, Patient


class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Врач")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Пациент")
    comment = models.CharField(max_length=500, verbose_name="Комментарий")
    rating = models.IntegerField(verbose_name="Рейтинг")
    date = models.DateField(verbose_name="Дата отзыва")

    def __str__(self):
        return f"Отзыв {self.id}"

    class Meta:
        unique_together = ('doctor', 'patient')
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

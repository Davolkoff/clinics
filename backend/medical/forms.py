from django import forms
from medical.models import Diagnosis


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['diagnosis_name']  # Выбираем только диагноз

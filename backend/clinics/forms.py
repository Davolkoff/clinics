from django import forms
from clinics.models import Clinic


class ClinicSelectForm(forms.Form):
    clinic = forms.ModelChoiceField(queryset=Clinic.objects.all(), label="Выберите клинику")


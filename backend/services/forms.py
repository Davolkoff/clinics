from django import forms
from .models import Service
from appointments.models import ServiceForAppointment


class ServiceSelectForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        required=False,
        label="Услуга",
        empty_label="-- Выберите услугу --"
    )


class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceForAppointment
        fields = ['service', 'quantity']  # Услуга и её количество
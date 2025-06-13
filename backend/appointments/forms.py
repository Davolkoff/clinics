from django import forms
from .models import Appointment
from users.models import Patient, Doctor


class AppointmentSelectForm(forms.Form):
    appointment = forms.ModelChoiceField(queryset=Appointment.objects.none(), label="Выберите приём")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Если пользователь пациент
            if hasattr(user, 'patient_profile'):
                self.fields['appointment'].queryset = Appointment.objects.filter(patient=user.patient_profile)
            # Если пользователь врач
            elif hasattr(user, 'doctor_profile'):
                self.fields['appointment'].queryset = Appointment.objects.filter(doctor=user.doctor_profile)


class AppointmentFormForDoctor(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'appointment_date', 'appointment_time']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        if doctor:
            self.fields['patient'].queryset = Patient.objects.all()


class AppointmentFormForPatient(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.all()

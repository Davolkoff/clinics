from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doctor, Patient
from services.models import DoctorSpeciality


class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    last_name = forms.CharField(max_length=50, required=True, label="Фамилия")
    first_name = forms.CharField(max_length=50, required=True, label="Имя")
    middle_name = forms.CharField(max_length=50, required=True, label="Отчество")
    birth_date = forms.DateField(
        required=True,
        label="Дата рождения",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    policy_number = forms.CharField(max_length=20, required=True, label="Номер полиса")
    phone_number = forms.CharField(max_length=15, required=True, label="Телефон")

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')  # Убираем username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Устанавливаем email как username
        if commit:
            user.save()
        return user


class DoctorForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")
    specialities = forms.ModelMultipleChoiceField(
        queryset=DoctorSpeciality.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        label="Специализации"
    )
    
    class Meta:
        model = Doctor
        fields = ['clinic', 'last_name', 'first_name', 'middle_name', 'email', 'photo', 'specialities']
        widgets = {
            'photo': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'form-control-file'
            }),
            'middle_name': forms.TextInput(attrs={
                'placeholder': 'Отчество (необязательно)'
            })
        }
        labels = {
            'photo': 'Фотография врача',
        }
        help_texts = {
            'photo': 'Рекомендуемый размер: 300x300px, формат JPG или PNG',
        }


class DoctorSelectForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), label="Выберите врача")


class PatientSelectionForm(forms.Form):

    patient = forms.ModelChoiceField(queryset=Patient.objects.none(), label="Выберите пациента")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'doctor_profile'):
            self.fields['patient'].queryset = Patient.objects.all()
from django.contrib import admin
from .models import ServiceForAppointment, Appointment, Payment
from medical.models import Diagnosis


# Register your models here.
class ServiceForAppointmentInline(admin.TabularInline):
    model = ServiceForAppointment
    extra = 1


class DiagnosisInline(admin.TabularInline):
    model = Diagnosis
    extra = 1

class AppointmentAdmin(admin.ModelAdmin):
    inlines = [DiagnosisInline, ServiceForAppointmentInline]
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time')

admin.site.register(Appointment, AppointmentAdmin)

admin.site.register(Payment)
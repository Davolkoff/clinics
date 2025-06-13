from django.contrib import admin
from .models import DoctorSpecialityRelation, DoctorService, Service, DoctorSpeciality


class DoctorSpecialityRelationInline(admin.TabularInline):
    model = DoctorSpecialityRelation
    extra = 1  # Число пустых форм для добавления новых специальностей
    fields = ['speciality']  # Только поле 'speciality' будет отображаться


class DoctorServiceInline(admin.TabularInline):
    model = DoctorService
    extra = 1
    fields = ['service']


admin.site.register(Service)
admin.site.register(DoctorSpeciality)
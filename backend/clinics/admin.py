from django.contrib import admin
from .models import Phone, Clinic


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1


class ClinicAdmin(admin.ModelAdmin):
    inlines = [PhoneInline]  # Подключаем Inline к модели Clinic
    list_display = ('name', 'address', 'working_hours')  # Поля для отображения в списке
    search_fields = ('name', 'address')


admin.site.register(Clinic, ClinicAdmin)

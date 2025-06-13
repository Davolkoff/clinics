from django.contrib import admin
from services.admin import DoctorSpecialityRelationInline, DoctorServiceInline
from .models import Doctor, Patient
from django.utils.html import format_html

# class DoctorAdmin(admin.ModelAdmin):
#     inlines = [DoctorSpecialityRelationInline, DoctorServiceInline]
#     list_display = ('last_name', 'first_name', 'middle_name', 'clinic')


class DoctorAdmin(admin.ModelAdmin):
    inlines = [DoctorSpecialityRelationInline, DoctorServiceInline]
    list_display = ('last_name', 'first_name', 'middle_name', 'clinic', 'display_photo')
    # readonly_fields = ('display_photo_preview',)
    
    # Добавляем миниатюру в список
    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.photo.url)
        return "Нет фото"
    display_photo.short_description = 'Фото'

admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient)


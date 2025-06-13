from django.urls import path
from .views import (
    clinic_info_view,
    download_clinic_info
)


urlpatterns = [
    path('', clinic_info_view, name='clinic_info'),
    path('download/<int:clinic_id>/', download_clinic_info, name='download_clinic_info'),
]

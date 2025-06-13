from django.urls import path
from .views import (
    doctors_by_service_view,
    download_doctors_by_service
)


urlpatterns = [
    path('doctors_by_service/', doctors_by_service_view, name='doctors_by_service'),
    path('doctors_by_service/download/<int:service_id>/', download_doctors_by_service,
         name='download_doctors_by_service')
]

from django.urls import path
from .views import (
    appointment_info_view,
    download_appointment_info,
    appointment_management,
    payments_view
)


urlpatterns = [
    path('', appointment_info_view, name='appointment_info'),
    path('download/<int:appointment_id>/', download_appointment_info, name='download_appointment_info'),
    path('manage/', appointment_management, name='appointment_management'),
    path('payments/', payments_view, name='payments_view'),
]

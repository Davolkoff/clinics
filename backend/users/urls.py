from django.urls import path
from .views import (
    register,
    login_view,
    create_doctor,
    doctor_info_view,
    download_doctor_info,
    patient_info_view,
    download_patient_info,
    custom_logout_view
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('create_doctor/', create_doctor, name='create_doctor'),
    path('doctor_info/', doctor_info_view, name='doctor_info'),
    path('doctor_info/download/<int:doctor_id>/', download_doctor_info, name='download_doctor_info'),
    path('patient_info/', patient_info_view, name='patient_info'),
    path('download_patient_info/<int:patient_id>/', download_patient_info, name='download_patient_info'),
]

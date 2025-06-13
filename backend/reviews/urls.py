from django.urls import path
from .views import reviews_view, download_reviews


urlpatterns = [
    path('', reviews_view, name='reviews'),
    path('download/<int:doctor_id>/', download_reviews, name='download_reviews'),
]

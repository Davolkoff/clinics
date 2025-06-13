import csv
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from users.forms import DoctorSelectForm
from .models import Review


def reviews_view(request):
    # Создаем форму для выбора врача
    form = DoctorSelectForm(request.GET or None)
    reviews = None
    doctor = None

    if form.is_valid():
        doctor = form.cleaned_data['doctor']
        reviews = Review.objects.filter(doctor=doctor)

    return render(request, 'reviews/reviews.html', {'form': form, 'reviews': reviews, 'doctor': doctor})


def download_reviews(request, doctor_id):
    reviews = Review.objects.filter(doctor_id=doctor_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="reviews_{doctor_id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Пациент', 'Комментарий', 'Рейтинг', 'Дата'])  # Заголовок столбцов

    for review in reviews:
        writer.writerow([review.patient, review.comment, review.rating, review.date])

    return response


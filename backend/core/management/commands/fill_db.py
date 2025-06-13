from django.core.management.base import BaseCommand
from appointments.models import *
from clinics.models import *
from medical.models import *
from reviews.models import *
from services.models import *
from users.models import *
from datetime import date, time
from django.core.files import File
from django.conf import settings
import os
from django.core.files.images import ImageFile


class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными'

    def handle(self, *args, **kwargs):
        
        User.objects.create_superuser(
            username='dav35@tpu.ru',
            email='dav35@tpu.ru',
            password='1'
        )
        self.stdout.write(self.style.SUCCESS(f'Администратор создан'))

        patient1 = Patient.objects.create(
            user=User.objects.create_user(
                username='test_patient1@mail.ru',
                email='test_patient1@mail.ru',
                password='test_patient1@mail.ru'
            ),
            last_name="Писарева",
            first_name="Валентина",
            middle_name="Олеговна",
            birth_date=date(2002, 3, 2),
            policy_number=123456789,
            phone_number="89528898750",
            email='test_patient1@mail.ru'
        )

        patient2 = Patient.objects.create(
            user=User.objects.create_user(
                username='test_patient2@mail.ru',
                email='test_patient2@mail.ru',
                password='test_patient2@mail.ru'
            ),
            last_name="Волков",
            first_name="Даниил",
            middle_name="Алексеевич",
            birth_date=date(2002, 9, 13),
            policy_number=123456789,
            phone_number="89527932000",
            email='test_patient2@mail.ru'
        )

        self.stdout.write(self.style.SUCCESS(f'Пациенты созданы'))

        vitamin_b_analysis = AnalysisName.objects.create(name="Анализ на витамин B")
        vitamin_c_analysis = AnalysisName.objects.create(name="Анализ на витамин C") 
        covid_analysis = AnalysisName.objects.create(name="Анализ на ковид")
        allerg_analysis = AnalysisName.objects.create(name="Анализ на аллергены")

        self.stdout.write(self.style.SUCCESS(f'Виды анализов созданы'))

        Analysis.objects.create(
            patient=patient1,
            analysis_name=vitamin_b_analysis,
            result="В пределах нормы",
            analysis_date=date(2025,2,15)
        )

        Analysis.objects.create(
            patient=patient1,
            analysis_name=vitamin_c_analysis,
            analysis_date=date(2025,5,1)
        )

        Analysis.objects.create(
            patient=patient2,
            analysis_name=covid_analysis,
            result="Отрицательный",
            analysis_date=date(2025,4,3)
        )

        self.stdout.write(self.style.SUCCESS(f'Анализы созданы'))

        eye_doctor = DoctorSpeciality.objects.create(name="Офтальмолог")
        brain_doctor = DoctorSpeciality.objects.create(name="Психолог")
        teeth_doctor = DoctorSpeciality.objects.create(name="Стоматолог")
        heart_doctor = DoctorSpeciality.objects.create(name="Кардиолог")

        self.stdout.write(self.style.SUCCESS(f'Специальности врачей созданы'))

        med_art = Clinic.objects.create(name="Мед-Арт",address="ул. Усова, 13", working_hours="08:00-21:00")
        sibmedcentr = Clinic.objects.create(name="СибМедЦентр",address="Красноармейская ул., 92/1", working_hours="08:00-20:00")
        zdorovje = Clinic.objects.create(name="Здоровье",address="ул. Котовского, 19", working_hours="09:00-18:00")

        self.stdout.write(self.style.SUCCESS(f'Клиники созданы'))

        Phone.objects.create(phone_number="83822564465", clinic=med_art, note="Регистратура")
        Phone.objects.create(phone_number="83822434346", clinic=sibmedcentr, note="Регистратура")
        Phone.objects.create(phone_number="83822902202", clinic=zdorovje, note="Многопрофильный центр")
        Phone.objects.create(phone_number="83822975111", clinic=zdorovje, note="Центр современной медицины")

        self.stdout.write(self.style.SUCCESS(f'Номера телефонов добавлены'))

        image_path = os.path.join(settings.MEDIA_ROOT, 'users','doctors', 'doctor1.jpg')

        with open(image_path, 'rb') as image_file:
            doctor1 = Doctor.objects.create(
                user=User.objects.create_user(
                    username='test_doctor1@mail.ru',
                    email='test_doctor1@mail.ru',
                    password='test_doctor1@mail.ru'
                ),
                clinic=zdorovje,
                last_name="Петров",
                first_name="Виталий",
                middle_name="Евгеньевич",
                photo=ImageFile(image_file, name='doctor1.jpg')
            )

        image_path = os.path.join(settings.MEDIA_ROOT, 'users','doctors', 'doctor2.jpg')

        with open(image_path, 'rb') as image_file:
            doctor2 = Doctor.objects.create(
                user=User.objects.create_user(
                    username='test_doctor2@mail.ru',
                    email='test_doctor2@mail.ru',
                    password='test_doctor2@mail.ru'
                ),
                clinic=sibmedcentr,
                last_name="Федоров",
                first_name="Ибрагим",
                middle_name="Степанович",
                photo=ImageFile(image_file, name='doctor2.jpg')
            )

        self.stdout.write(self.style.SUCCESS(f'Врачи добавлены'))

        DoctorSpecialityRelation.objects.create(doctor=doctor1,speciality=eye_doctor)
        DoctorSpecialityRelation.objects.create(doctor=doctor1,speciality=teeth_doctor)
        DoctorSpecialityRelation.objects.create(doctor=doctor2,speciality=brain_doctor)

        self.stdout.write(self.style.SUCCESS(f'Врачи связаны со специальностями'))

        Review.objects.create(doctor=doctor1, patient=patient1,comment="Отличный специалист, всем рекомендую", rating=5, date=date(2024,9,1))
        Review.objects.create(doctor=doctor1, patient=patient2,comment="Вылечил. Теперь здоровый", rating=5, date=date(2024,9,30))

        Review.objects.create(doctor=doctor2, patient=patient1,comment="Спасибо доктору, всё хорошо", rating=4, date=date(2024,4,5))
        Review.objects.create(doctor=doctor2, patient=patient2,comment="Всё круто, всем доволен", rating=5, date=date(2024,2,20))

        self.stdout.write(self.style.SUCCESS(f'Отзывы добавлены'))

        consult = Service.objects.create(name="Консультация", price=1000)
        threapy = Service.objects.create(name="Терапия", price=1500)
        diagnostics = Service.objects.create(name="Диагностика", price=5000)
        uncaries = Service.objects.create(name="Лечение зуба", price=3000)

        self.stdout.write(self.style.SUCCESS(f'Услуги добавлены'))

        DoctorService.objects.create(service=consult, doctor=doctor1)
        DoctorService.objects.create(service=consult, doctor=doctor2)
        DoctorService.objects.create(service=threapy, doctor=doctor2)
        DoctorService.objects.create(service=diagnostics, doctor=doctor1)
        DoctorService.objects.create(service=uncaries, doctor=doctor1)

        self.stdout.write(self.style.SUCCESS(f'Услуги привязаны к докторам'))

        caries = DiagnosisName.objects.create(name="Кариес")
        pulpit = DiagnosisName.objects.create(name="Пульпит")
        depression = DiagnosisName.objects.create(name="Депрессия")
        tachycardia = DiagnosisName.objects.create(name="Тахикардия")

        self.stdout.write(self.style.SUCCESS(f'Диагнозы добавлены'))

        appointment_1 = Appointment.objects.create(
            patient=patient2,
            doctor=doctor2,
            appointment_date=date(2025,2,15),
            appointment_time=time(12,0)
        )

        appointment_2 = Appointment.objects.create(
            patient=patient2,
            doctor=doctor1,
            appointment_date=date(2025,4,7),
            appointment_time=time(14,30)
        )
        
        appointment_3 = Appointment.objects.create(
            patient=patient1,
            doctor=doctor1,
            appointment_date=date(2025,5,14),
            appointment_time=time(13,5)
        )

        self.stdout.write(self.style.SUCCESS(f'Приемы добавлены'))

        ServiceForAppointment.objects.create(service=threapy,appointment=appointment_1,quantity=1)
        ServiceForAppointment.objects.create(service=consult,appointment=appointment_2,quantity=1)
        ServiceForAppointment.objects.create(service=consult,appointment=appointment_3,quantity=1)
        ServiceForAppointment.objects.create(service=uncaries,appointment=appointment_3,quantity=4)

        self.stdout.write(self.style.SUCCESS(f'Услуги привязаны к приемам'))

        Diagnosis.objects.create(diagnosis_name=depression, appointment=appointment_1)
        Diagnosis.objects.create(diagnosis_name=tachycardia, appointment=appointment_2)
        Diagnosis.objects.create(diagnosis_name=pulpit, appointment=appointment_3)
        Diagnosis.objects.create(diagnosis_name=caries, appointment=appointment_3)

        self.stdout.write(self.style.SUCCESS(f'Диагнозы поставлены'))

        card = PaymentType.objects.create(name="Оплата картой")
        cash = PaymentType.objects.create(name="Оплата наличными")

        self.stdout.write(self.style.SUCCESS(f'Добавлены способы оплаты'))

        Payment.objects.create(appointment=appointment_1, payment_type=card, payment_date=date(2025,3,20))
        Payment.objects.create(appointment=appointment_2, payment_type=cash, payment_date=date(2025,3,23))

        self.stdout.write(self.style.SUCCESS(f'Оплата произведена'))
        
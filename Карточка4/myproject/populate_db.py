import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from phonebook.models import Abonent

# Очищаем существующие записи (опционально)
Abonent.objects.all().delete()

# Добавляем 3 записи (Задание 4.1)
abonents = [
    Abonent(
        last_name='Иванов',
        first_name='Петр',
        patronymic='Сергеевич',
        birth_date=date(1985, 5, 15),
        phone='+7 (495) 555-12-34',
        address='ул. Советская, д. 10, кв. 5'
    ),
    Abonent(
        last_name='Петрова',
        first_name='Анна',
        patronymic='Ивановна',
        birth_date=date(1990, 8, 22),
        phone='+7 (495) 123-45-67',
        address='ул. Ленина, д. 15, кв. 8'
    ),
    Abonent(
        last_name='Сидоров',
        first_name='Михаил',
        patronymic='Петрович',
        birth_date=date(1978, 3, 10),
        phone='+7 (495) 555-67-89',
        address='ул. Советская, д. 25, кв. 12'
    ),
]

for abonent in abonents:
    abonent.save()

print("База данных успешно заполнена!")
print(f"Добавлено записей: {Abonent.objects.count()}")
import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import datetime


def example3(request):
    """Информация о файле (аналог PHP infoFile)"""
    # Путь к файлу (например, к самому views.py)
    file_path = os.path.join(settings.BASE_DIR, 'lr23', 'views.py')

    file_info = {
        'file_path': file_path,
        'exists': os.path.exists(file_path),
        'is_file': os.path.isfile(file_path) if os.path.exists(file_path) else False,
        'is_dir': os.path.isdir(file_path) if os.path.exists(file_path) else False,
        'is_readable': os.access(file_path, os.R_OK) if os.path.exists(file_path) else False,
        'is_writable': os.access(file_path, os.W_OK) if os.path.exists(file_path) else False,
        'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
        'last_modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) if os.path.exists(
            file_path) else None,
        'last_accessed': datetime.datetime.fromtimestamp(os.path.getatime(file_path)) if os.path.exists(
            file_path) else None,
    }

    return render(request, 'lr23/example3.html', {'file_info': file_info})


def example4(request):
    """Чтение файла построчно"""
    file_path = os.path.join(settings.BASE_DIR, 'lr23', 'static', 'lr23', 'ex1.txt')
    lines = []

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

    return render(request, 'lr23/example4.html', {'lines': lines})


# Функции для работы с датой и временем
def get_russian_weekday(date_obj=None):
    """Возвращает день недели на русском языке"""
    if date_obj is None:
        date_obj = datetime.datetime.now()

    # Получаем английское сокращение
    weekday_en = date_obj.strftime('%a')

    # Преобразуем в русский
    weekdays = {
        'Mon': 'понедельник',
        'Tue': 'вторник',
        'Wed': 'среда',
        'Thu': 'четверг',
        'Fri': 'пятница',
        'Sat': 'суббота',
        'Sun': 'воскресенье',
    }

    return weekdays.get(weekday_en, 'неизвестно')


def datetime_example(request):
    """Вывод текущей даты и времени"""
    now = datetime.datetime.now()

    context = {
        'date_short': now.strftime('%d.%m.%Y'),  # 01.04.2023
        'time': now.strftime('%H:%M:%S'),
        'weekday': get_russian_weekday(now),
        'now': now,
    }

    return render(request, 'lr23/datetime_example.html', context)


def weekday_form(request):
    """Форма для определения дня недели"""
    weekday_russian = None

    if request.method == 'POST':
        date_str = request.POST.get('date')
        if date_str:
            try:
                # Пробуем разные форматы даты
                try:
                    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    date_obj = datetime.datetime.strptime(date_str, '%d.%m.%Y')

                weekday_russian = get_russian_weekday(date_obj)
            except ValueError:
                weekday_russian = "Ошибка в формате даты"

    return render(request, 'lr23/weekday_form.html', {
        'weekday_russian': weekday_russian,
        'today': datetime.datetime.now().strftime('%Y-%m-%d')
    })

def example1(request):
    return render(request, 'lr23/example1.html')

def example2(request):
    return render(request, 'lr23/example2.html', {'result': 56})
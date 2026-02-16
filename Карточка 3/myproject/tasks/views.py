from django.shortcuts import render
from datetime import datetime
import math
from .models import Product

VARIANT_NUMBER = 16


def index(request):
    context = {}
    return render(request, 'tasks/index.html', context)


def task1_days_of_week(request):
    """Задание 2: Массив дней недели и текущий день"""
    days_of_week = {
        1: 'Понедельник',
        2: 'Вторник',
        3: 'Среда',
        4: 'Четверг',
        5: 'Пятница',
        6: 'Суббота',
        7: 'Воскресенье'
    }

    current_day_num = datetime.now().isoweekday()
    current_day = days_of_week[current_day_num]

    context = {
        'days_of_week': days_of_week,
        'current_day': current_day,
        'current_day_num': current_day_num
    }
    return render(request, 'tasks/task1_days.html', context)


def task2_while_loop(request):
    """Задание 3: Цикл while для вывода ФИО"""
    n = VARIANT_NUMBER
    surname = "Иванов"
    name = "Иван"

    results = []
    i = 0
    while i < n + 5:
        results.append({
            'number': i + 1,
            'full_name': f"{surname} {name}"
        })
        i += 1

    context = {
        'n': n,
        'results': results,
        'total_count': n + 5
    }
    return render(request, 'tasks/task2_while.html', context)


def task3_arrays(request):
    """Задание 4: Работа с ассоциативным массивом"""
    # Создаем продукты в БД, если их нет
    if Product.objects.count() == 0:
        Product.objects.create(name='Хлеб', price=5000)
        Product.objects.create(name='Молоко', price=8000)
        Product.objects.create(name='Сметана', price=7000)

    products = Product.objects.all()

    # Получаем цену молока
    milk_product = Product.objects.filter(name='Молоко').first()
    milk_price = milk_product.price if milk_product else 0

    # Суммарная стоимость
    total_price = sum(product.price for product in products)

    context = {
        'products': products,
        'milk_price': milk_price,
        'total_price': total_price
    }
    return render(request, 'tasks/task3_arrays.html', context)


def task4_strings(request):
    """Задание 5: Работа со строками"""
    n = VARIANT_NUMBER
    s1 = "Я люблю Беларусь"
    s2 = "Я учусь в Политехническом колледже"

    # 1. Длина строки
    length_s1 = len(s1)

    # 2. Выделить n-ый символ и его ASCII код
    if 1 <= n <= len(s1):
        nth_char = s1[n - 1]
        ascii_code = ord(nth_char)
    else:
        nth_char = "Ошибка: недопустимый индекс"
        ascii_code = "—"

    # 3. Замена букв "ю" на "№"
    s1_modified = s1.replace('ю', '№')

    context = {
        'n': n,
        's1': s1,
        's2': s2,
        'length_s1': length_s1,
        'nth_char': nth_char,
        'ascii_code': ascii_code,
        's1_modified': s1_modified
    }
    return render(request, 'tasks/task4_strings.html', context)


def calculate_f(x):
    """Пользовательская функция для расчета по формуле"""
    try:
        if x <= 7:
            return -x*x
        else:  # x > 7
            if x == 0:
                raise ZeroDivisionError("Деление на ноль!")
            result = 2**x/(x*x-9)
            if math.isnan(result) or math.isinf(result):
                raise ValueError("Недопустимый результат вычисления")
            return round(result, 2)
    except ZeroDivisionError as e:
        return str(e)
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"Неизвестная ошибка: {e}"


def task5_function(request):
    """Задание 6: Пользовательская функция"""
    # Тестовые значения для x
    test_values = [5, 7, 10, 0, 14, -3, 2.5]

    results = []
    for x in test_values:
        try:
            result = calculate_f(x)
            if isinstance(result, (int, float)):
                results.append({
                    'x': x,
                    'result': result,
                    'error': False,
                    'error_message': ''
                })
            else:
                results.append({
                    'x': x,
                    'result': None,
                    'error': True,
                    'error_message': result
                })
        except Exception as e:
            results.append({
                'x': x,
                'result': None,
                'error': True,
                'error_message': str(e)
            })

    context = {
        'results': results,
        'formula': 'F(x) = 2*x при x ≤ 7, F(x) = 2*7/x при x > 7'
    }
    return render(request, 'tasks/task5_function.html', context)


def all_tasks(request):
    """Объединение всех заданий на одной странице"""
    n = VARIANT_NUMBER

    # Задание 2
    days_of_week = {
        1: 'Понедельник', 2: 'Вторник', 3: 'Среда',
        4: 'Четверг', 5: 'Пятница', 6: 'Суббота', 7: 'Воскресенье'
    }
    current_day_num = datetime.now().isoweekday()
    current_day = days_of_week[current_day_num]

    # Задание 3
    while_results = []
    i = 0
    while i < n + 5:
        while_results.append(f"{i + 1}. Уланович Владислав")
        i += 1

    # Задание 4
    products = [
        {'name': 'Хлеб', 'price': 5000},
        {'name': 'Молоко', 'price': 8000},
        {'name': 'Сметана', 'price': 7000},
    ]
    milk_price = next(p['price'] for p in products if p['name'] == 'Молоко')
    total_price = sum(p['price'] for p in products)

    # Задание 5
    s1 = "Я люблю Беларусь"
    length_s1 = len(s1)
    if 1 <= n <= len(s1):
        nth_char = s1[n - 1]
        ascii_code = ord(nth_char)
    else:
        nth_char = "—"
        ascii_code = "—"
    s1_modified = s1.replace('ю', '№')

    # Задание 6
    test_values = [5, 7, 10, 0, 14]
    func_results = []
    for x in test_values:
        result = calculate_f(x)
        if isinstance(result, (int, float)):
            func_results.append({'x': x, 'result': result, 'error': False})
        else:
            func_results.append({'x': x, 'result': result, 'error': True})

    context = {
        'n': n,
        'current_day': current_day,
        'while_results': while_results,
        'products': products,
        'milk_price': milk_price,
        'total_price': total_price,
        's1': s1,
        'length_s1': length_s1,
        'nth_char': nth_char,
        'ascii_code': ascii_code,
        's1_modified': s1_modified,
        'func_results': func_results,
    }
    return render(request, 'tasks/all_tasks.html', context)
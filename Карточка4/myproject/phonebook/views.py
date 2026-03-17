import os
from django.shortcuts import render, redirect
from .forms import UserDataForm
from .models import Abonent


def form_view(request):
    """
    Представление для отображения формы и обработки POST-запроса
    """
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            user_name = form.cleaned_data['user_name']
            gender = form.cleaned_data['gender']  # Новое поле
            maiden_name = form.cleaned_data['maiden_name']

            # Сохраняем в сессию
            request.session['user_name'] = user_name
            request.session['gender'] = gender
            request.session['maiden_name'] = maiden_name

            return redirect('session_page')
    else:
        form = UserDataForm()

    return render(request, 'phonebook/form_page.html', {'form': form})


def session_view(request):
    """
    Представление для страницы сессии
    """
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    # Получаем данные из сессии
    user_name = request.session.get('user_name', 'Не указано')
    gender = request.session.get('gender', 'Не указано')  # Получаем пол
    maiden_name = request.session.get('maiden_name', 'Не указано')

    # Записываем в файл
    a = 5
    b = 7
    sum_ab = a + b
    product_ab = a * b

    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '1.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"Сумма {a} и {b} = {sum_ab}\n")
        f.write(f"Произведение {a} и {b} = {product_ab}\n")

    context = {
        'session_id': session_id,
        'user_name': user_name,
        'gender': gender,  # Передаем пол в шаблон
        'maiden_name': maiden_name,
        'sum_ab': sum_ab,
        'product_ab': product_ab,
    }

    return render(request, 'phonebook/session_page.html', context)


def abonent_list(request):
    """
    Представление для отображения списка абонентов
    """
    filtered_abonents = Abonent.objects.filter(
        address__icontains='Советская',
        phone__contains='5'
    )

    all_abonents = Abonent.objects.all()

    context = {
        'filtered_abonents': filtered_abonents,
        'all_abonents': all_abonents,
    }

    return render(request, 'phonebook/abonent_list.html', context)
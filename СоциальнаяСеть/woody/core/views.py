from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def notifications(request):
    return render(request, 'core/notifications.html', {'title': 'Уведомления'})


@login_required
def search_page(request):
    return render(request, 'core/search.html', {'title': 'Поиск'})


def custom_404_view(request, exception=None):
    return render(request, 'core/404.html', status=404)
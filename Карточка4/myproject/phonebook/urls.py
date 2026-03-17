from django.urls import path
from . import views


urlpatterns = [
    path('', views.form_view, name='form_page'),
    path('session/', views.session_view, name='session_page'),
    path('abonents/', views.abonent_list, name='abonent_list'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_tasks, name='all_tasks'),
    path('days/', views.task1_days_of_week, name='task1_days'),
    path('while/', views.task2_while_loop, name='task2_while'),
    path('arrays/', views.task3_arrays, name='task3_arrays'),
    path('strings/', views.task4_strings, name='task4_strings'),
    path('function/', views.task5_function, name='task5_function'),
]
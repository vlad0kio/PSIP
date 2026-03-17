from django.urls import path
from . import views

app_name = 'lr23'

urlpatterns = [
    path('example1/', views.example1, name='example1'),
    path('example2/', views.example2, name='example2'),
    path('example3/', views.example3, name='example3'),
    path('example4/', views.example4, name='example4'),
    path('datetime/', views.datetime_example, name='datetime_example'),
    path('weekday/', views.weekday_form, name='weekday_form'),
]
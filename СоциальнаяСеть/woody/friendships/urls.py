from django.urls import path
from . import views

urlpatterns = [
    path('', views.friends_list, name='friends'),
    path('search/', views.search_friends, name='search_friends'),
    path('send/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('remove/<int:user_id>/', views.remove_friend, name='remove_friend'),
]
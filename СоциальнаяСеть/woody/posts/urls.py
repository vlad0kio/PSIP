from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('feed/', views.feed, name='feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
]
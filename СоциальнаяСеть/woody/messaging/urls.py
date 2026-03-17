from django.urls import path
from . import views

urlpatterns = [
    path('', views.messages_page, name='messages'),
    path('<int:user_id>/', views.conversation, name='conversation'),
    path('send/<int:user_id>/', views.send_message, name='send_message'),
    path('new/<int:conversation_id>/<int:last_message_id>/', views.get_new_messages, name='get_new_messages'),
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
]
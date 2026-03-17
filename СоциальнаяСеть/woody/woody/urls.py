from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Приложения
    path('', include('posts.urls')),  # Главная страница - лента
    path('accounts/', include('accounts.urls')),
    path('friends/', include('friendships.urls')),
    path('messages/', include('messaging.urls')),
    path('', include('core.urls')),  # Уведомления, поиск и т.д.
]

handler404 = 'core.views.custom_404_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
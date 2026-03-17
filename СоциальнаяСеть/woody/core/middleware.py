# core/middleware.py
from django.utils import timezone
from django.apps import apps


class OnlineStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                # Получаем модель Profile через apps
                Profile = apps.get_model('accounts', 'Profile')
                profile = request.user.profile
                profile.last_seen = timezone.now()
                profile.is_online = True
                profile.save(update_fields=['last_seen', 'is_online'])
            except (Profile.DoesNotExist, AttributeError):
                pass

        response = self.get_response(request)
        return response
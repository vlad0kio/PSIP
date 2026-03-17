# core/context_processors.py
from django.apps import apps
from django.db.models import Q, Count


def notifications_processor(request):
    """Добавляет количество непрочитанных сообщений в контекст"""
    if request.user.is_authenticated:
        # Получаем модель Conversation через apps
        Conversation = apps.get_model('messaging', 'Conversation')

        # Считаем количество бесед с непрочитанными сообщениями
        unread_total = Conversation.objects.filter(
            participants=request.user
        ).annotate(
            unread_count=Count('messages', filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user))
        ).filter(unread_count__gt=0).count()

        return {
            'unread_total': unread_total
        }
    return {}
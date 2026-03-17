from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Max, Count

from accounts.models import Profile
from .models import Conversation, Message


@login_required
def messages_page(request):
    conversations = Conversation.objects.filter(
        participants=request.user
    ).annotate(
        last_message_time=Max('messages__created_at'),
        unread_count=Count('messages', filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user))
    ).order_by('-last_message_time')

    for conv in conversations:
        conv.other_user = conv.get_other_participant(request.user)
        conv.last_message = conv.get_last_message()

        try:
            conv.other_user.profile = Profile.objects.get(user=conv.other_user)
        except Profile.DoesNotExist:
            conv.other_user.profile = Profile.objects.create(user=conv.other_user)

    context = {
        'title': 'Сообщения',
        'conversations': conversations,
        'unread_total': sum(conv.unread_count for conv in conversations)
    }
    return render(request, 'messaging/messages.html', context)


@login_required
def conversation(request, user_id):
    try:
        other_user = User.objects.get(id=user_id)

        conversation_obj = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user
        ).distinct().first()

        if not conversation_obj:
            conversation_obj = Conversation.objects.create()
            conversation_obj.participants.add(request.user, other_user)

        messages_list = Message.objects.filter(
            conversation=conversation_obj
        ).select_related('sender').order_by('created_at')

        unread_messages = messages_list.filter(
            sender=other_user,
            is_read=False
        )
        for msg in unread_messages:
            msg.mark_as_read()

        try:
            other_user.profile = Profile.objects.get(user=other_user)
        except Profile.DoesNotExist:
            other_user.profile = Profile.objects.create(user=other_user)

        context = {
            'title': f'Чат с {other_user.username}',
            'conversation': conversation_obj,
            'other_user': other_user,
            'messages': messages_list,
        }
        return render(request, 'messaging/conversation.html', context)

    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден')
        return redirect('messages_page')


@login_required
@require_POST
def send_message(request, user_id):
    try:
        other_user = User.objects.get(id=user_id)
        text = request.POST.get('text', '').strip()

        if not text:
            return JsonResponse({'success': False, 'error': 'Сообщение не может быть пустым'})

        conversation_obj = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user
        ).distinct().first()

        if not conversation_obj:
            conversation_obj = Conversation.objects.create()
            conversation_obj.participants.add(request.user, other_user)

        message = Message.objects.create(
            conversation=conversation_obj,
            sender=request.user,
            text=text
        )

        conversation_obj.save()

        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'text': text,
            'created_at': message.created_at.strftime('%H:%M'),
            'sender_username': request.user.username,
            'sender_avatar': request.user.profile.avatar.url if hasattr(request.user,
                                                                        'profile') and request.user.profile.avatar else ''
        })

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Пользователь не найден'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def get_new_messages(request, conversation_id, last_message_id):
    try:
        conversation_obj = Conversation.objects.get(
            id=conversation_id,
            participants=request.user
        )

        new_messages = Message.objects.filter(
            conversation=conversation_obj,
            id__gt=last_message_id
        ).select_related('sender').order_by('created_at')

        other_user = conversation_obj.get_other_participant(request.user)
        for msg in new_messages.filter(sender=other_user):
            msg.mark_as_read()

        messages_data = []
        for msg in new_messages:
            messages_data.append({
                'id': msg.id,
                'text': msg.text,
                'sender_id': msg.sender.id,
                'sender_username': msg.sender.username,
                'is_own': msg.sender == request.user,
                'created_at': msg.created_at.strftime('%H:%M'),
                'avatar': msg.sender.profile.avatar.url if hasattr(msg.sender,
                                                                   'profile') and msg.sender.profile.avatar else ''
            })

        return JsonResponse({
            'success': True,
            'messages': messages_data,
            'count': len(messages_data)
        })

    except Conversation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Беседа не найдена'})


@login_required
def start_conversation(request, user_id):
    try:
        other_user = User.objects.get(id=user_id)
        return redirect('conversation', user_id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден')
        return redirect('messages_page')
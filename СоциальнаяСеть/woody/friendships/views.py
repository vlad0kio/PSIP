from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from accounts.models import Profile
from .models import FriendRequest, Friendship


@login_required
def friends_list(request):
    friendships = Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    )

    friends_list = []
    for friendship in friendships:
        if friendship.user1 == request.user:
            friend = friendship.user2
        else:
            friend = friendship.user1

        try:
            friend.profile = Profile.objects.get(user=friend)
        except Profile.DoesNotExist:
            friend.profile = Profile.objects.create(user=friend)

        friends_list.append(friend)

    incoming_requests = FriendRequest.objects.filter(
        to_user=request.user,
        status='pending'
    ).select_related('from_user')

    outgoing_requests = FriendRequest.objects.filter(
        from_user=request.user,
        status='pending'
    ).select_related('to_user')

    context = {
        'title': 'Друзья',
        'friends': friends_list,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
    }
    return render(request, 'friendships/friends.html', context)


@login_required
def search_friends(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        results = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)

    for user in results:
        user.is_friend = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2=user)) |
            (Q(user1=user) & Q(user2=request.user))
        ).exists()

        user.sent_request = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=user,
            status='pending'
        ).exists()

        user.received_request = FriendRequest.objects.filter(
            from_user=user,
            to_user=request.user,
            status='pending'
        ).first()

        try:
            user.profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            user.profile = Profile.objects.create(user=user)

    context = {
        'title': 'Поиск друзей',
        'query': query,
        'results': results,
    }

    return render(request, 'friendships/search_friends.html', context)


@login_required
@require_POST
def send_friend_request(request, user_id):
    try:
        to_user = get_object_or_404(User, id=user_id)

        if request.user.id == user_id:
            return JsonResponse({
                'success': False,
                'message': 'Нельзя отправить запрос самому себе'
            })

        are_friends = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2=to_user)) |
            (Q(user1=to_user) & Q(user2=request.user))
        ).exists()

        if are_friends:
            return JsonResponse({
                'success': False,
                'message': 'Вы уже друзья с этим пользователем'
            })

        existing_request = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=to_user
        ).first()

        if existing_request:
            if existing_request.status == 'pending':
                return JsonResponse({
                    'success': False,
                    'message': 'Запрос уже отправлен и ожидает ответа'
                })
            elif existing_request.status == 'accepted':
                return JsonResponse({
                    'success': False,
                    'message': 'Вы уже друзья с этим пользователем'
                })
            elif existing_request.status == 'rejected':
                existing_request.status = 'pending'
                existing_request.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Запрос отправлен повторно'
                })

        reverse_request = FriendRequest.objects.filter(
            from_user=to_user,
            to_user=request.user,
            status='pending'
        ).first()

        if reverse_request:
            return JsonResponse({
                'success': False,
                'message': 'Этот пользователь уже отправил вам запрос на дружбу'
            })

        FriendRequest.objects.create(
            from_user=request.user,
            to_user=to_user,
            status='pending'
        )

        return JsonResponse({
            'success': True,
            'message': 'Запрос на дружбу отправлен'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Ошибка: {str(e)}'
        })


@login_required
@require_POST
def accept_friend_request(request, request_id):
    try:
        friend_request = get_object_or_404(
            FriendRequest,
            id=request_id,
            to_user=request.user,
            status='pending'
        )

        Friendship.objects.create(
            user1=friend_request.from_user,
            user2=friend_request.to_user
        )

        friend_request.status = 'accepted'
        friend_request.save()

        return JsonResponse({
            'success': True,
            'message': f'Вы теперь друзья с {friend_request.from_user.username}'
        })

    except Exception:
        return JsonResponse({
            'success': False,
            'message': 'Заявка не найдена'
        })


@login_required
@require_POST
def reject_friend_request(request, request_id):
    try:
        friend_request = get_object_or_404(
            FriendRequest,
            id=request_id,
            to_user=request.user,
            status='pending'
        )

        friend_request.status = 'rejected'
        friend_request.save()

        return JsonResponse({
            'success': True,
            'message': 'Заявка отклонена'
        })

    except Exception:
        return JsonResponse({
            'success': False,
            'message': 'Заявка не найдена'
        })


@login_required
@require_POST
def remove_friend(request, user_id):
    try:
        friend = get_object_or_404(User, id=user_id)

        Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2=friend)) |
            (Q(user1=friend) & Q(user2=request.user))
        ).delete()

        return JsonResponse({
            'success': True,
            'message': f'Пользователь {friend.username} удален из друзей'
        })

    except Exception:
        return JsonResponse({
            'success': False,
            'message': 'Пользователь не найден'
        })
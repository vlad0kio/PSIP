from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Post, Like, Comment


def feed(request):
    """
    Лента постов - доступна всем пользователям
    Для неавторизованных показываем посты без возможности взаимодействия
    """
    posts_list = Post.objects.all().order_by('-created_at')

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Базовая информация для всех пользователей
    for post in page_obj:
        post.likes_count = Like.objects.filter(post=post).count()
        post.comments_count = Comment.objects.filter(post=post).count()
        post.recent_comments = Comment.objects.filter(post=post)[:2]

        # Информация о лайке только для авторизованных
        if request.user.is_authenticated:
            post.is_liked = Like.objects.filter(post=post, user=request.user).exists()
        else:
            post.is_liked = False

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'user_authenticated': request.user.is_authenticated,
    }

    return render(request, 'posts/feed.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Post.objects.create(author=request.user, content=content)
    return redirect('feed')


@login_required
@require_POST
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()

        likes_count = Like.objects.filter(post=post).count()

        return JsonResponse({
            'success': True,
            'likes_count': likes_count,
            'is_liked': created
        })

    except Post.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Пост не найден'
        }, status=404)


@login_required
@require_POST
def add_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        text = request.POST.get('text', '').strip()

        if not text:
            return JsonResponse({'success': False, 'error': 'Комментарий не может быть пустым'})

        comment = Comment.objects.create(post=post, author=request.user, text=text)

        avatar_url = ''
        if hasattr(request.user, 'profile') and request.user.profile.avatar:
            avatar_url = request.user.profile.avatar.url

        return JsonResponse({
            'success': True,
            'username': request.user.username,
            'avatar_url': avatar_url,
            'text': text,
            'comment_id': comment.id
        })
    except Post.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Пост не найден'
        }, status=404)
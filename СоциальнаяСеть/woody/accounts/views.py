from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as auth_logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from posts.models import Post, Like, Comment
from .models import Profile


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password1 or not password2:
            return render(request, 'accounts/register.html', {'error': 'Все поля обязательны'})

        if len(password1) < 8:
            return render(request, 'accounts/register.html', {'error': 'Пароль должен содержать минимум 8 символов'})

        if password1 != password2:
            return render(request, 'accounts/register.html', {'error': 'Пароли не совпадают'})

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Пользователь с таким именем уже существует'})

        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {'error': 'Пользователь с таким email уже существует'})

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            login(request, user)
            messages.success(request, f'Аккаунт {username} создан!')
            return redirect('feed')

        except Exception as e:
            return render(request, 'accounts/register.html', {'error': f'Ошибка при создании пользователя: {str(e)}'})

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('feed')
        else:
            return render(request, 'accounts/login.html', {'error': 'Неверное имя пользователя или пароль'})

    return render(request, 'accounts/login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
        is_own_profile = (user == request.user)

        user_posts = Post.objects.filter(author=user).order_by('-created_at')

        paginator = Paginator(user_posts, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        for post in page_obj:
            post.likes_count = Like.objects.filter(post=post).count()
            post.comments_count = Comment.objects.filter(post=post).count()
            post.is_liked = Like.objects.filter(post=post, user=request.user).exists()

        context = {
            'profile_user': user,
            'is_own_profile': is_own_profile,
            'posts': page_obj,
            'page_obj': page_obj,
            'is_paginated': paginator.num_pages > 1,
        }

        return render(request, 'accounts/profile.html', context)

    except User.DoesNotExist:
        return render(request, 'core/user_not_found.html', {
            'username': username,
            'title': 'Пользователь не найден'
        })


@login_required
def settings(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()

        if hasattr(user, 'profile'):
            user.profile.bio = request.POST.get('bio', user.profile.bio)
            user.profile.save()

        messages.success(request, 'Настройки сохранены!')
        return redirect('settings')

    return render(request, 'accounts/settings.html')
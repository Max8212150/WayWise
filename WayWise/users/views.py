from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, EmailLoginForm


def register_view(request):
    """
    Регистрация пользователя.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Логиним автоматически после регистрации
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')  # на главную
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    Вход пользователя (требует email и пароль).
    """
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы вошли в систему!')
                return redirect('home')
    else:
        form = EmailLoginForm()  # пустая форма при GET-запросе
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """
    Выход из учётной записи.
    """
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')


@login_required
def profile(request):
    # Передача данных о пользователе в шаблон
    user = request.user
    return render(request, 'users/profile.html', {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    })

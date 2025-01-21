from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import PasswordResetView

from .forms import UserRegistrationForm
from .models import *
from .forms import *

# Функция для главной страницы 
def main_page(request):
    if request.user.is_authenticated:
        my_task = Task.objects.filter(executor = request.user)
        return render(request, 'TM/main_page.html', {'my_task': my_task})
    else:
        return render(request, 'TM/main_page.html')

def introductoryPage(request):
    return render(request, 'TM/introductoryPage.html')

# Функция для регистрации
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Вы успешно зарегистрировались!!')
            return redirect(reverse('main_page'))
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = UserRegistrationForm()
    return render(request, 'TM/register.html', {'form': form})

# Создание ного проекта
def new_project(request):
    if request.method == 'POST':
        form = new_project_forms(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            if request.user.is_authenticated:
                project.creator = request.user

            project.save()
            print('Сохранино')
            messages.success(request, 'Успешно сохранено')
            return redirect(reverse('new_project'))
    else:
        form = new_project_forms()
    return render(request, 'TM/new_project.html', {'form': form})

# Создания новой задачи для проекта
def new_task(request):
    return render(request, 'TM/new_task.html')

# Задачи которые я делаю
def tasksIDo(request):
    return render(request, 'TM/tasksIdo.html')

# Создание новой подзадачи
def new_subtask(request):
    return render(request, 'TM/new_subtask.html')

# мои собственные задачи
def my_own_task(request):
    return render(request, "TM/my_own_task.html")

# Создаем собственную задачу
def new_my_task(request):
    return render(request, "TM/new_my_task.html")

# Настройки
def settings(request):
    return render(request, 'TM/settings.html')


# Не знаю зачем пока это нужно, скорее всего уберу 
class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        messages.success(self.request, 'Вам было отправлено электронное письмо с инструкциями по сбросу вашего пароля.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка при обработке запроса.')
        return super().form_invalid(form)

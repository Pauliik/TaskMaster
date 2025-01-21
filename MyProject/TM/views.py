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
        project_form = New_project_forms(request.POST)
        task_form = New_projectTask_forms(request.POST)
        if project_form.is_valid() and task_form.is_valid():
            project = project_form.save(commit=False)
            if request.user.is_authenticated:
                project.creator = request.user
            project.save()
            task = task_form.save(commit=False)
            task.project = project
            task.save()
            print('Сохранино')
            messages.success(request, 'Успешно сохранено')
            return redirect(reverse('new_project'))
    else:
        project_form = New_project_forms()
        task_form = New_projectTask_forms()
    return render(request, 'TM/new_project.html', {'project_form': project_form, 'task_form': task_form})

# Создания новой задачи для проекта
def new_task(request):
    if request.method == 'POST':
        form = New_task_forms(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, 'Успешно сохранено')
            return render(request, 'TM/new_task.html', {'form': form})
    form = New_task_forms()

    return render(request, 'TM/new_task.html', {'form': form})

# Задачи которые я делаю
def tasksIDo(request):
    if request.user.is_authenticated:
        my_task = Task.objects.filter(executor = request.user)
        return render(request, 'TM/tasksIDo.html', {'my_task': my_task})

    

# Создание новой подзадачи
def new_sub(request):
    if request.method == 'POST':
        form = New_sub_forms(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            if request.user.is_authenticated:
                subtask.creator = request.user
            messages.success(request, 'Успешно сохранено')
            return render(request, 'TM/new_task.html', {'form': form})
    else:
        form = New_sub_forms()

    return render(request, 'TM/new_task.html', {'form': form})
    

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

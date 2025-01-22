from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponseForbidden

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
            messages.success(request, f'Проект {project} успешно сохранен')
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
            messages.success(request, f'Задача {task} успешна сохранена')
            return render(request, 'TM/new_task.html', {'form': form})
    form = New_task_forms()

    return render(request, 'TM/new_task.html', {'form': form})

# Мои проекты
def my_project(request):
    if request.user.is_authenticated:
        myproject= Project.objects.filter(creator = request.user)
        return render(request, 'TM/my_project.html', {'myproject': myproject})

# Задачи которые я делаю
def tasksIDo(request):
    if request.user.is_authenticated:
        my_task = Task.objects.filter(executor = request.user)
        return render(request, 'TM/tasksIDo.html', {'my_task': my_task})

# Создание новой подзадачи
def new_subtask(request, task_id):
    task = get_object_or_404(Task, id = task_id)
    
    if request.method == 'POST':
        form = New_subtask_forms(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            if request.user.is_authenticated:
                subtask.task = task
                subtask.creator = request.user
                subtask.save()
            messages.success(request, 'Успешно сохранено')
            return redirect(reverse('new_subtask', kwargs={'task_id': task.id}))
    else:
        form = New_subtask_forms()

    return render(request, 'TM/new_subtask.html', {'form': form})
    

# мои собственные задачи
def my_own_task(request):
    if request.user.is_authenticated:
        my_task = Mytask.objects.filter(creator = request.user)
        return render(request, 'TM/my_own_task.html', {'my_task': my_task})
    

# Создаем собственную задачу
def new_my_task(request):
    if request.method == 'POST':
        form = New_my_task_form(request.POST)
        if form.is_valid():
            mytask = form.save(commit=False)
            if request.user.is_authenticated:
                mytask.creator = request.user
            mytask.save()
            print('Сохранино')
            messages.success(request, f'Успешно сохранено {mytask.name_task}')
            return redirect(reverse('new_my_task'))
    else:
        form = New_my_task_form()
    return render(request, 'TM/new_my_task.html', {'form': form,})

# Создаем собственные подзодачи
def new_my_subtask(request, task_id):
    mytask = get_object_or_404(Mytask, id = task_id)
    
    if request.method == 'POST':
        form = New_my_subtask_forms(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            if request.user.is_authenticated:
                subtask.task = mytask
                subtask.creator = request.user
                subtask.save()
            messages.success(request, f'Успешно сохранено {subtask.name_subtask}')
            return redirect(reverse('new_my_subtask', kwargs={'task_id': mytask.id}))
    else:
        form = New_my_subtask_forms()

    return render(request, 'TM/new_my_subtask.html', {'form': form})

# Настройки
def settings(request):
    return render(request, 'TM/settings.html')


# Редактирование проекта
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        project_form = New_project_forms(request.POST, instance=project) # instance=project Подставляет данные
        if project_form.is_valid():
            project_form.save()
            messages.success(request, f'Проект {project.name} успешно обновлен')
            return redirect(reverse('my_project'))
        else:
            messages.error(request, 'Произошла ошибка при обновлении проекта!')
    else:
        project_form = New_project_forms(instance=project) 

    return render(request, 'Edit/edit_project.html', {'project_form': project_form,})

# Редактирование задачи
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task_form = Edit_task_form(request.POST, instance=task) # instance=project Подставляет данные
        if task_form.is_valid():
            task_form.save()
            messages.success(request, f'Проект {task.name_task} успешно обновлен')
            return redirect(reverse('my_project'))
        else:
            messages.error(request, 'Произошла ошибка при обновлении проекта!')
    else:
        task_form = Edit_task_form(instance=task) 

    return render(request, 'Edit/edit_task.html', {'task_form': task_form,})

# Редактирование мои задачи
def edit_my_task(request, task_id):
    task = get_object_or_404(Mytask, id=task_id)
    
    if request.method == 'POST':
        task_form = Edit_my_task_form(request.POST, instance=task) # instance=project Подставляет данные
        if task_form.is_valid():
            task_form.save()
            messages.success(request, f'Проект {task.name_task} успешно обновлен')
            return redirect(reverse('my_own_task'))
        else:
            messages.error(request, 'Произошла ошибка при обновлении проекта!')
    else:
        task_form = Edit_my_task_form(instance=task) 

    return render(request, 'Edit/edit_my_task.html', {'task_form': task_form,})

# Редактирование мои подзадачи для моих задочь
def edit_mysubtask(request, subtask_id):
    subtask = get_object_or_404(Mysubtask, id=subtask_id)
    
    if request.method == 'POST':
        subtask_form = Edit_mysubtask_form(request.POST, instance=subtask) # instance=project Подставляет данные
        if subtask_form.is_valid():
            subtask_form.save()
            messages.success(request, f'Проект {subtask.name_subtask} успешно обновлен')
            return redirect(reverse('my_own_task'))
        else:
            messages.error(request, 'Произошла ошибка при обновлении проекта!')
    else:
        subtask_form = Edit_mysubtask_form(instance=subtask) 

    return render(request, 'Edit/edit_mysubtask.html', {'subtask_form': subtask_form,})

# Редактирование мои подзадачи
def edit_subtask(request, subtask_id):
    subtask = get_object_or_404(Subtask, id=subtask_id)
    
    if request.method == 'POST':
        subtask_form = Edit_subtask_form(request.POST, instance=subtask) # instance=project Подставляет данные
        if subtask_form.is_valid():
            subtask_form.save()
            messages.success(request, f'Проект {subtask.name_sub} успешно обновлен')
            return redirect(reverse('tasksIDo'))
        else:
            messages.error(request, 'Произошла ошибка при обновлении проекта!')
    else:
        subtask_form = Edit_subtask_form(instance=subtask) 

    return render(request, 'Edit/edit_subtask.html', {'subtask_form': subtask_form,})

# Удалить проект
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user == project.creator:
        if request.method == 'POST':
            project.delete()
            messages.success(request, f'Проект {project.name} успешно удален.')
            return redirect(reverse('my_project'))
        return render(request, 'delete/delete_project.html', {'project': project})
    else:
       return HttpResponseForbidden("У вас нет прав на удаление этого проекта.")
    
# Удалить задачу
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user == task.project.creator:
        if request.method == 'POST':
            task.delete()
            messages.success(request, f'Проект {task.name_task} успешно удален.')
            return redirect(reverse('my_project'))
        return render(request, 'delete/delete_task.html', {'task': task})
    else:
       return HttpResponseForbidden("У вас нет прав на удаление этого проекта.")
    
# Удалить мою задачу
def delete_my_task(request, task_id):
    task = get_object_or_404(Mytask, id=task_id)

    if request.user == task.creator:
        if request.method == 'POST':
            task.delete()
            messages.success(request, f'Проект {task.name_task} успешно удален.')
            return redirect(reverse('my_own_task'))
        return render(request, 'delete/delete_my_task.html', {'task': task})
    else:
       return HttpResponseForbidden("У вас нет прав на удаление этого проекта.")

# Удалить мою подзадачу для моей задыч
def delete_my_subtask(request, subtask_id):
    subtask = get_object_or_404(Mysubtask, id=subtask_id)

    if request.user == subtask.task.creator:
        if request.method == 'POST':
            subtask.delete()
            messages.success(request, f'Проект {subtask.name_subtask} успешно удален.')
            return redirect(reverse('my_own_task'))
        return render(request, 'delete/delete_my_subtask.html', {'subtask': subtask})
    else:
       return HttpResponseForbidden("У вас нет прав на удаление этого проекта.")
    
# Удалить мою подзадачу
def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(Subtask, id=subtask_id)

    if request.user == subtask.creator:
        if request.method == 'POST':
            subtask.delete()
            messages.success(request, f'Проект {subtask.name_sub} успешно удален.')
            return redirect(reverse('tasksIDo'))
        return render(request, 'delete/delete_subtask.html', {'subtask': subtask})
    else:
       return HttpResponseForbidden("У вас нет прав на удаление этого проекта.")









# Не знаю зачем пока это нужно, скорее всего уберу 
class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        messages.success(self.request, 'Вам было отправлено электронное письмо с инструкциями по сбросу вашего пароля.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка при обработке запроса.')
        return super().form_invalid(form)

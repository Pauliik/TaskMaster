from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.mail import send_mail
from django.forms.models import model_to_dict

from django.http import JsonResponse

from .models import *
from .forms import *
from .filters import *



# Функция для главной страницы 
def main_page(request, project_name=None):
    if request.user.is_authenticated:
        comments = []
        project = None
        if project_name:
            project = get_object_or_404(Project, name = project_name)
            comments = TaskComment.objects.filter(project = project)
        if request.method == 'POST':
            form = Comment_form(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                if request.user.is_authenticated:
                    comment.project = project
                    comment.author_comment = request.user
                    comment.save()
                return redirect(reverse('main_page', kwargs={'project_name': project.name}))
        else:
            form = Comment_form()

        if request.user.is_staff:
            projects = Project.objects.filter(creator = request.user)
            return render(request, 'TM/main_page.html', {'projects': projects, 'comments': comments, 'form': form, 'project': project},)
            
        else:
            task = Task.objects.filter(executor = request.user)
            projects = Project.objects.filter(tasks__in = task).distinct()
            return render(request, 'TM/main_page.html', {'projects': projects, 'comments': comments,'form': form, 'project': project})
    else:
        return render(request, 'TM/introductoryPage.html')

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
        
        try:
            if project_form.is_valid() and task_form.is_valid():
                project = project_form.save(commit=False)
                task = task_form.save(commit=False)
                if project.end_date < task.due_date:
                    raise ValidationError('Проект не может быть сдал раньше чем задача к нему!!!')
                if request.user.is_authenticated:
                    project.creator = request.user
                project.save()
            
                task.project = project
                task.save()
                send_mail(
                    'У вас появилась новое задание!',
                    f'Руководитель {request.user} выдал вам задание {task.name_task} котророе нужно выполнить до {task.due_date}',
                    'pasha@inbox.ru',
                    [task.executor.email],
                    fail_silently=False,
                )
                messages.success(request, f'Проект {project} успешно сохранен')
                return redirect(reverse('new_project'))
        except ValidationError as e:
            messages.error(request, e.message)

    else:
        project_form = New_project_forms()
        task_form = New_projectTask_forms()
    return render(request, 'TM/new_project.html', {'project_form': project_form, 'task_form': task_form})

# Создания новой задачи для проекта
def new_task(request, project_name):
    if request.user.is_authenticated:
        project = get_object_or_404(Project, name = project_name)
        if request.method == 'POST':
            form = New_task_forms(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.project = project
                task.save()
                send_mail(
                    'У вас появилась новое задание!',
                    f'Руководитель {request.user} выдал вам задание {task.name_task} котророе нужно выполнить до {task.due_date}',
                    'pasha@inbox.ru',
                    [task.executor.email],
                    fail_silently=False,
                )
                messages.success(request, f'Задача {task} успешна сохранена')
                return redirect(reverse('new_task', kwargs={'project_name': project.name}))
        else:  
            form = New_task_forms()
        return render(request, 'TM/new_task.html', {'form': form})

# Проекты
def my_project(request):
    if request.user.is_authenticated:
        check = Project.objects.filter(creator = request.user).exists()
        queryset = Project.objects.filter(creator = request.user)
        filter = Project_filter(request.GET, queryset=queryset)
        myproject = filter.qs
        return render(request, 'TM/my_project.html', {'myproject': myproject, 'filter': filter, 'check': check})

# Задания к проектам
def my_project_task(request, project_name): 
    if request.user.is_authenticated:
        project = get_object_or_404(Project, name = project_name)        
        check = Task.objects.filter(project = project).exists()
        queryset = Task.objects.filter(project = project)
        filter = Task_project_filter(request.GET, queryset=queryset)
        tasks = filter.qs
        return render(request, 'TM/my_project_task.html', {'tasks': tasks, 'filter': filter, 'check': check, 'project_name': project.name})

# Задачи которые я делаю
def tasksIDo(request):    
    if request.user.is_authenticated:
        check = Task.objects.filter(executor = request.user).exists()
        queryset = Task.objects.filter(executor = request.user)
        filter = Task_filter(request.GET, queryset=queryset)
        my_task = filter.qs

        if request.method == 'POST':
            form = Send_file_form(request.POST, request.FILES)
            task_id = request.POST.get('task_id') # Получаем ID задачи из POST запроса
            task = get_object_or_404(Task, id = task_id)
            if form.is_valid():          
                Myfile = request.FILES['file']

                #Создаем экземпляр
                file_task = FileTask(
                task = task,
                file=Myfile,
                sender = request.user
                )
                file_task.save()

                send_mail(
                    f'Увожвемый {request.user} ',
                    f'Рабочий {request.user} переслал вам {file_task.file} файл с выполненой задачей {task.name_task} которая находится в проекте {task.project.name}',
                    'pasha@inbox.ru',
                    [task.project.creator.email],
                    fail_silently=False,
                )

                messages.success(request, 'Файл успешно сохранено')
                return redirect(reverse('tasksIDo'))
        else:
            form = Send_file_form()
    return render(request, 'TM/tasksIDo.html', {'my_task': my_task, 'form': form, 'filter': filter, 'check': check})

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
        check = Mytask.objects.filter(creator = request.user).exists()
        queryset = Mytask.objects.filter(creator = request.user)
        filter = Mytask_filter(request.GET, queryset=queryset)
        my_task = filter.qs
        return render(request, 'TM/my_own_task.html', {'my_task': my_task, 'filter': filter, 'check': check})

    
# Создаем собственную задачу
def new_my_task(request):
    if request.method == 'POST':
        form = New_my_task_form(request.POST)
        if form.is_valid():
            mytask = form.save(commit=False)
            if request.user.is_authenticated:
                mytask.creator = request.user
            mytask.save()
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
        project_form = Edit_project_forms(request.POST, instance=project) # instance=project Подставляет данные
        if project_form.is_valid():
            project_form.save()
            messages.success(request, f'Проект {project.name} успешно обновлен')
            return redirect(reverse('my_project'))
        #else:
           # messages.error(request, 'Произошла ошибка при обновлении проекта!')
    else:
        project_form = Edit_project_forms(instance=project) 

    return render(request, 'Edit/edit_project.html', {'project_form': project_form,})

# Редактирование задачи
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project_name = request.GET.get('project_name')
    initial_data = model_to_dict(task) # Создает словарь из таблицы
    old_name, old_email = task.executor.username, task.executor.email

    if request.method == 'POST':
        task_form = Edit_task_form(request.POST, instance=task) # instance=project Подставляет данные
        if task_form.is_valid():
            task_form.save()
            new_data = model_to_dict(task)
            if (initial_data == new_data) == False:
                if initial_data['executor'] == new_data['executor']:
                    send_mail(
                        f'Уважаемый {task.executor.username}',
                        f'Руководитель {request.user} Отредактировал задание {task.name_task}',
                        'pasha@inbox.ru',
                        [task.executor.email],
                        fail_silently=False,
                    )
                else:
                    send_mail(
                        f'Уважаемый {old_name}',
                        f'Руководитель {request.user} передал задание {task.name_task} другому' ,
                        'pasha@inbox.ru',
                        [old_email],
                        fail_silently=False,
                    )

                    send_mail(
                        f'Уважаемый {task.executor.username}',
                        f'Руководитель {request.user} передал вам выполнять новое задания {task.name_task} заместо {old_name}',
                        'pasha@inbox.ru',
                        [task.executor.email],
                        fail_silently=False,
                    )
            messages.success(request, f'Проект {task.name_task} успешно обновлен') 
            return redirect(reverse('my_project_task', kwargs={'project_name': project_name}))
        #else:
            #messages.error(request, 'Произошла ошибка при обновлении проекта!')
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
        #else:
            #messages.error(request, 'Произошла ошибка при обновлении проекта!')
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
    project_name = request.GET.get('project_name')
    if request.user == task.project.creator:
        if request.method == 'POST':
            task.delete()

            send_mail(
                        f'Уважаемый {task.executor.username}',
                        f'Руководитель {request.user} удалил задание {task.name_task} из проекта {task.project.name}',
                        'pasha@inbox.ru',
                        [task.executor.email],
                        fail_silently=False,
                    )
            
            messages.success(request, f'Проект {task.name_task} успешно удален.')
            return redirect(reverse('my_project_task', kwargs={'project_name': project_name}))
        return render(request, 'delete/delete_task.html', {'task': task, 'project_name': project_name})
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

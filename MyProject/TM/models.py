from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length = 255, unique = True, verbose_name = 'Название проекта')
    description = models.TextField(verbose_name = 'Описание проекта')
    end_date = models.DateField(verbose_name = 'Дфта окончания')
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'created_projects', verbose_name = 'Создатель')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата создания')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name
    
class Task(models.Model):
    PRIORITY = [ 
        ('high', 'Высокий'),
        ('medium', 'Средний'),
        ('low', 'Низкий')
    ]

    ACCOMPLISHMENTS_STATUS = [   # СТАТУС ДОСТИЖЕНИЙ
        ('in_progress', 'в работе'),
        ('on_review', 'На проверке'),
        ('completed', 'Выполнена'),
        ('canceled', 'Отменена')
    ]

    project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = 'tasks', verbose_name = 'Проект')
    name_task = models.CharField(max_length= 255, verbose_name = 'Название задачи')
    description = models.TextField(blank= True, verbose_name = 'Опмсание задачи')
    priority = models.CharField(max_length = 15, choices = PRIORITY, default = 'medium', verbose_name = 'Приоритет')
    status = models.CharField(max_length = 20, choices = ACCOMPLISHMENTS_STATUS, default = 'in_progress', verbose_name = 'Статус')
    executor = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'assigned_tasks', verbose_name = 'Исполнитель')
    due_date = models.DateField(verbose_name = 'Срок выполнения')
    #creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'created_tasks', verbose_name = 'Создатель')
    date_creation = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')
    date_update = models.DateTimeField(auto_now = True, verbose_name = 'Дата обновления')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name_task
    
class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete = models.CASCADE, related_name = 'subtask', verbose_name = 'Задача')
    name_sub = models.CharField(max_length = 255, verbose_name = 'Название подзадачи')
    description = models.TextField(null = True, blank= True, verbose_name = 'Опмсание задачи')
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'creator_subtask', verbose_name = 'Создатель')
    status = models.BooleanField(default = False, verbose_name = 'Статус выполнения')
    date_creation = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')

    class Meta:
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадачи'

    def __str__(self):
        return self.name_sub
    
class TaskComment(models.Model):
    #task = models.ForeignKey(Task, on_delete = models.CASCADE, related_name = 'comments', verbose_name = 'Задфчв')
    project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = 'comments', verbose_name = 'Проект') #??????
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Автор комментария')
    comment_text = models.TextField(verbose_name = 'Текст коментария')
    date_creation = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')

    class Meta:
        verbose_name = 'Комментарий к задаче'
        verbose_name_plural = 'Комментарии к задаче'

    def __str__(self):
        return f'Коментарий оставил {self.user.username} к задаче {self.task.name_task}'
    
class FileTask(models.Model):
    task = models.ForeignKey(Task, on_delete = models.CASCADE, related_name = 'fileTasks', verbose_name = 'Задача')
    file = models.FileField(upload_to = 'task_attachments/', verbose_name = 'Файл')
    sender = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'sender_fileTasks', verbose_name = 'Отправитель')
    date_creation = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')

    class Meta:
        verbose_name = 'Файл для задачи'
        verbose_name_plural = 'Файлы для задачи'

    def __str__(self):
        return self.file.name # Должен вкрнуть имя файла ????
    
class Mytask(models.Model):
    PRIORITY = [ 
        ('high', 'Высокий'),
        ('medium', 'Средний'),
        ('low', 'Низкий')
    ]
    name_task = models.CharField(max_length= 255, verbose_name = 'Название задачи')
    description = models.TextField(blank= True, verbose_name = 'Опмсание задачи')
    priority = models.CharField(max_length = 15, choices = PRIORITY, default = 'medium', verbose_name = 'Приоритет')
    due_date = models.DateField(verbose_name = 'Срок выполнения')
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'mytask', verbose_name = 'Создатель')
    date_creation = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')
    date_update = models.DateTimeField(auto_now = True, verbose_name = 'Дата обновления')

    class Meta:
        verbose_name = 'Моя задача'
        verbose_name_plural = 'Мои задачи'

    def __str__(self):
        return self.name_task
    
class Mysubtask(models.Model):
    task = models.ForeignKey(Mytask, on_delete = models.CASCADE, related_name = 'mysubtasks', verbose_name = 'Задача')
    name_subtask = models.CharField(max_length = 255, verbose_name = 'Название подзадачи')
    description = models.TextField(null = True, blank= True, verbose_name = 'Опмсание задачи')
    #creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'creator_mysubtasks', verbose_name = 'Создатель')
    status = models.BooleanField(default = False, verbose_name = 'Статус выполнения')
    date_creation = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата создания')

    class Meta:
        verbose_name = 'моя подзадача'
        verbose_name_plural = 'Мои подзадачи'

    def __str__(self):
        return self.name_subtask
                               
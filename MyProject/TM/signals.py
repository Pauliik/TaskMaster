from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now

from datetime import datetime, timedelta
from threading import Thread

import os
import time
import schedule
from .models import *

@receiver(post_save, sender = Task)
def Task_edit_signals(sender, instance, created, **kwargs):
    if not created:
        None

@receiver(pre_delete, sender = Project)
def Project_delete_signals(sender, instance, **kwargs):
    unique_executors = set()

    for task in instance.tasks.all():
        if task.executor:
            unique_executors.add(task.executor)
        for file in task.fileTasks.all():
            try:
                path = os.path.join(settings.MEDIA_ROOT, str(file))
                os.remove(path)
            except:
                None

    if unique_executors:
        for executor in unique_executors:
            send_mail(
                f'Уважаемый {executor.username}',
                f'Руководитель {instance.creator.username} удалил проект {instance.name} так что все задания к нему были удалены',
                'pasha@inbox.ru',
                [executor.email],
                fail_silently=False,
            )
        
# Задачи для дополнительного патока который будет отправлять сообщения рабочим о том что им завтра нужно сдавать работу
def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target = function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator

# Ваша функция, которую нужно запускать в отдельном потоке
@start_new_thread
def scheduler():
    schedule.every().day.at("07:53").do(my_job) # Каждый день в 15:00

    while True:
        schedule.run_pending()
        time.sleep(1)

def my_job():
    print(f"Работа выполняется в отдельном потоке в {datetime.now()}")
    # Получаем завтрашнюю дату
    tomorrow = now().date() + timedelta(days=1)
    # Фильтруем задачи, у которых дедлайн завтра
    tasks = Task.objects.filter(due_date=tomorrow, status='in_progress')
    if tasks:
        for task in tasks:           
            send_mail(
                f'Уважаемый {task.executor.username}',
                f'Завтра до 15:00 нужно сдать задачу {task.name_task}',
                'pasha@inbox.ru',
                [task.executor.email],
                fail_silently=False,
            )
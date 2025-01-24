from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail

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
            print(task.executor)
            unique_executors.add(task.executor)

    if unique_executors:
        for executor in unique_executors:
            send_mail(
                f'Уважаемый {executor.username}',
                f'Руководитель {instance.creator.username} удалил проект {instance.name} так что все задания к нему были удалены',
                'pasha@inbox.ru',
                [executor.email],
                fail_silently=False,
            )

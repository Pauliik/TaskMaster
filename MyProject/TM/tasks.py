from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import Task

@shared_task
def send_notification_email(task_id):
    print('2')
    try:
        task = Task.objects.get(id=task_id)
        user = task.executor
        if user:
            send_mail(
                f'Напоминание о задаче: {task.name_task}',
                f'Срок выполнения задачи {task.name_task} приближается (дата: {task.due_date})',
                'pasha@inbox.ru',
                [task.executor.email],
                fail_silently=False,
            )
            print('3')
    except Task.DoesNotExist:
        pass  # Запись в логи об ошибке

@shared_task
def check_due_dates():
    print('1')
    now = timezone.now().date()
    tomorrow = now + timedelta(days=1)
    tasks = Task.objects.filter(due_date=tomorrow, status='in_progress')
    for task in tasks:
        None
        #send_notification_email.delay(task.id)
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyProject.settings') # Замените your_project на имя своего проекта

app = Celery('MyProject')  # Замените your_project на имя своего проекта

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
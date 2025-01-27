# Generated by Django 5.1.5 on 2025-01-27 17:07

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mytask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_task', models.CharField(max_length=255, verbose_name='Название задачи')),
                ('description', models.TextField(blank=True, verbose_name='Описание задачи')),
                ('priority', models.CharField(choices=[('high', 'Высокий'), ('medium', 'Средний'), ('low', 'Низкий')], default='medium', max_length=15, verbose_name='Приоритет')),
                ('due_date', models.DateField(verbose_name='Срок выполнения')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mytask', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Моя задача',
                'verbose_name_plural': 'Мои задачи',
            },
        ),
        migrations.CreateModel(
            name='Mysubtask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_subtask', models.CharField(max_length=255, verbose_name='Название подзадачи')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание задачи')),
                ('status', models.BooleanField(default=False, verbose_name='Статус выполнения')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mysubtasks', to='TM.mytask', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'моя подзадача',
                'verbose_name_plural': 'Мои подзадачи',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название проекта')),
                ('description', models.TextField(verbose_name='Описание проекта')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
                ('key', models.CharField(default=uuid.uuid4, max_length=64, unique=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_projects', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_task', models.CharField(max_length=255, verbose_name='Название задачи')),
                ('description', models.TextField(blank=True, verbose_name='Описание  задачи')),
                ('priority', models.CharField(choices=[('high', 'Высокий'), ('medium', 'Средний'), ('low', 'Низкий')], default='medium', max_length=15, verbose_name='Приоритет')),
                ('status', models.CharField(choices=[('in_progress', 'в работе'), ('on_review', 'На проверке'), ('completed', 'Выполнена')], default='in_progress', max_length=20, verbose_name='Статус')),
                ('due_date', models.DateField(verbose_name='Срок выполнения')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('executor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='TM.project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.CreateModel(
            name='Subtask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_sub', models.CharField(max_length=255, verbose_name='Название подзадачи')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание задачи')),
                ('status', models.BooleanField(default=False, verbose_name='Статус выполнения')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator_subtask', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtask', to='TM.task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Подзадача',
                'verbose_name_plural': 'Подзадачи',
            },
        ),
        migrations.CreateModel(
            name='FileTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='work_file/', verbose_name='Файл')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender_fileTasks', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fileTasks', to='TM.task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Файл для задачи',
                'verbose_name_plural': 'Файлы для задачи',
            },
        ),
        migrations.CreateModel(
            name='TaskComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(verbose_name='Текст коментария')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('author_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='TM.project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Комментарий к задаче',
                'verbose_name_plural': 'Комментарии к задаче',
            },
        ),
    ]

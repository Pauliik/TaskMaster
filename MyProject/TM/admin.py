from django.contrib import admin
from .models import *

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'end_date', 'creator', 'date_creation')
    search_fields = ('name', 'creator')
    
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'name_task', 'description', 'priority', 'status', 'executor', 'due_date', 'creator', 'date_creation', 'date_update')
    search_fields = ('project', 'executor')

@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'name_subtask', 'status', 'date_creation')
    search_fields = ('task',)

@admin.register(TaskComment)
class TaskComentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author_comment', 'comment_text', 'date_creation')
    search_fields = ('task',)

@admin.register(FileTask)
class FileTaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'file', 'sender', 'date_creation')
    search_fields = ('task', 'file')



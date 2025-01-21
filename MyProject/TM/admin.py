from django.contrib import admin
from .models import *

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'end_date', 'creator', 'date_creation')
    search_fields = ('name', 'creator')
    
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'name_task', 'description', 'priority', 'status', 'executor', 'due_date', 'date_creation', 'date_update')
    search_fields = ('project', 'executor')

@admin.register(Sub)
class SubAdmin(admin.ModelAdmin):
    list_display = ('task', 'name_sub', 'description', 'creator', 'status', 'date_creation')
    search_fields = ('task',)

@admin.register(TaskComment)
class TaskComentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author_comment', 'comment_text', 'date_creation')
    search_fields = ('task', 'creator')

@admin.register(FileTask)
class FileTaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'file', 'sender', 'date_creation')
    search_fields = ('task', 'file')

@admin.register(Mytask)
class MytaskAdmin(admin.ModelAdmin):
    list_display = ('name_task', 'description', 'priority', 'due_date', 'creator', 'date_creation', 'date_update')
    search_fields = ('creator',)

@admin.register(Mysubtask)
class MysubtaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'name_subtask', 'creator', 'status', 'date_creation')
    search_fields = ('task', 'creator')



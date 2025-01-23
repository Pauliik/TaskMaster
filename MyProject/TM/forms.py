from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from .models import *

# Используется для регистрации         
class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким адресом электронной почты уже существует.')
        return email

# используется для edit_project и new_project
class New_project_forms(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'end_date']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),  # format='%Y-%m-%d' исправляет вставку времени из БД для редактирования  
        }

# используется для edit_project и new_project
class New_projectTask_forms(forms.ModelForm):
    class Meta:
        model = Task
        fields = [ 'name_task', 'description', 'priority', 'status', 'executor', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs = {'type': 'date'}),
        }

class New_task_forms(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'name_task', 'description', 'priority', 'status', 'executor', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs = {'type': 'date'}),
        }

class New_subtask_forms(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['name_sub', 'description']
        #widgets = {}

class New_my_task_form(forms.ModelForm):
    class Meta:
        model = Mytask
        fields = ['name_task', 'description', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs = {'type': 'date'}),
        }

class New_my_subtask_forms(forms.ModelForm):
    class Meta:
        model = Mysubtask
        fields = ['name_subtask', 'description']
        #widgets = {}

# Форма для редактирования задачи
class Edit_task_form(forms.ModelForm):
    class Meta:
        model = Task
        fields = [ 'name_task', 'description', 'priority', 'status', 'executor', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs = {'type': 'date'}, format='%Y-%m-%d'),
        }

# Форма для редактирование моих задач
class Edit_my_task_form(forms.ModelForm):
    class Meta:
        model = Mytask
        fields = ['name_task', 'description', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs = {'type': 'date'}, format='%Y-%m-%d'),
        }       

# Форма для редактирование моих подзадачь для моих задач
class Edit_mysubtask_form(forms.ModelForm):
    class Meta:
        model = Mysubtask
        fields = ['name_subtask', 'description', 'status']
        #widgets = {}

# Форма для редактирование моих подзадачь
class Edit_subtask_form(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['name_sub', 'description', 'status']
        #widgets = {}

# Форма для редактирование моих подзадачь
class Comment_form(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['comment_text']
        #widgets = {}


import os
# Форма для отправки файлов
class Send_file_form(forms.ModelForm):
    class Meta:
        model = FileTask
        fields = ['file']
        #widgets = {}

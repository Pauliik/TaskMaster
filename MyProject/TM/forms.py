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
    
class new_project_forms(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'end_date']
        widgets = {
            'end_date': forms.DateInput(attrs = {'type': 'date'}),
        }


        


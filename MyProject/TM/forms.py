from django import forms
from django.forms import DateInput, TimeInput
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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


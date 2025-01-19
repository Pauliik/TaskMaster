from django import forms
from django.forms import DateInput, TimeInput
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

        
class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


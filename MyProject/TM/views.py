from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import PasswordResetView

def introductoryPage(request):
    return render(request, 'TM/introductoryPage.html')

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Вы успешно зарегистрировались!!')
            return redirect(reverse('main_page'))
    else:
        form = UserRegistrationForm()
    return render(request, 'TM/register.html', {'form': form})

def main_page(request):
    return render(request, 'TM/main_page.html')


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        messages.success(self.request, 'Вам было отправлено электронное письмо с инструкциями по сбросу вашего пароля.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка при обработке запроса.')
        return super().form_invalid(form)

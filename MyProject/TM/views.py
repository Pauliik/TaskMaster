from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib import messages
from django.urls import reverse


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

from django.urls import path, include
from . import views, api
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.introductoryPage, name='introductoryPage'),
    path('register/', views.register_user, name='register'),
    path('main/', views.main_page, name='main_page'),


    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    

    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_reset_email.html",
        success_url=reverse_lazy("password_reset_done")
    ), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html",
        success_url=reverse_lazy("password_reset_complete")
    ), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name ='password_reset_complete'),
    

]
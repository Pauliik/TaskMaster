from django.urls import path, include
from . import views, api
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.introductoryPage, name='introductoryPage'),
    path('register/', views.register_user, name='register'),
    path('main/', views.main_page, name='main_page'),
    path('settings', views.settings, name = 'settings'),
    path('NewTask', views.new_task, name = 'new_task'),
    path('NewProject', views.new_project, name = 'new_project'),
    path('tasksIDo', views.tasksIDo, name = 'tasksIDo'),
    path('NewSubtask', views.new_sub, name = 'new_sub'),
    path('MyOwnTask', views.my_own_task, name = 'my_own_task'),
    path('NewMyTask', views.new_my_task, name = 'new_my_task'),


    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    

    #path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/', views.CustomPasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view( template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    

]
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
    path('NewSubtask/<int:task_id>/', views.new_subtask, name = 'new_subtask'),
    path('MyOwnTask', views.my_own_task, name = 'my_own_task'),
    path('NewMyTask', views.new_my_task, name = 'new_my_task'),
    path('NewMySubtask/<int:task_id>/', views.new_my_subtask, name = 'new_my_subtask'),
    path('MyProject', views.my_project, name = 'my_project'),
    path('Comment/<str:project_name>/', views.comment_project, name = 'comment'),

    # Для редактирования 
    path('EditProject/<int:project_id>/', views.edit_project, name = 'edit_project'),
    path('EditTask/<int:task_id>/', views.edit_task, name = 'edit_task'),
    path('EditMyTask/<int:task_id>/', views.edit_my_task, name = 'edit_my_task'),
    path('EditMySubtask/<int:subtask_id>/', views.edit_mysubtask, name = 'edit_mysubtask'),
    path('EditSubtask/<int:subtask_id>/', views.edit_subtask, name = 'edit_subtask'),

    # Для удаления
    path('DeleteProject/<int:project_id>/', views.delete_project, name = 'delete_project'),
    path('Deletetask/<int:task_id>/', views.delete_task, name = 'delete_task'),
    path('DeleteMytask/<int:task_id>/', views.delete_my_task, name = 'delete_my_task'),
    path('DeleteMySubtask/<int:subtask_id>/', views.delete_my_subtask, name = 'delete_my_subtask'),
    path('DeleteSubtask/<int:subtask_id>/', views.delete_subtask, name = 'delete_subtask'),

    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    

    #path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/', views.CustomPasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view( template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    

]
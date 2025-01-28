from django.urls import path
from . import views
from . import task_views

app_name = 'projects'

urlpatterns = [
    # Existing URLs
    path('', views.projects, name='projects'),
    path('new-project/', views.newProject, name='new-project'),
    path('new-task/', views.newTask, name='new-task'),
    
    # Task management URLs
    path('task-list/', task_views.task_list, name='task_list'),
    path('task/create/', task_views.create_task, name='create_task'),
    path('task/<int:task_id>/update/', task_views.update_task, name='update_task'),
    path('task/<int:task_id>/delete/', task_views.delete_task, name='delete_task'),
]
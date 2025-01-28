from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, Project, status
from django.contrib.auth.models import User
from django.urls import reverse

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'projects/task_list.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        project_id = request.POST.get('project')
        task_name = request.POST.get('task_name')
        assigned_users = request.POST.getlist('assign')
        status_value = request.POST.get('status')
        
        project = get_object_or_404(Project, id=project_id)
        task = Task.objects.create(
            project=project,
            task_name=task_name,
            status=status_value
        )
        task.assign.set(assigned_users)
        messages.success(request, 'Task created successfully!')
        return redirect('projects:task_list')
    
    projects = Project.objects.all()
    users = User.objects.all()
    return render(request, 'projects/task_form.html', {
        'projects': projects,
        'users': users,
        'status_choices': status,
    })

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.task_name = request.POST.get('task_name')
        task.status = request.POST.get('status')
        task.assign.set(request.POST.getlist('assign'))
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('projects:task_list')
    
    projects = Project.objects.all()
    users = User.objects.all()
    return render(request, 'projects/task_form.html', {
        'task': task,
        'projects': projects,
        'users': users,
        'status_choices': status,
    })

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('projects:task_list')
    return render(request, 'projects/task_confirm_delete.html', {'task': task})

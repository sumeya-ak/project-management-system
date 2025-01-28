from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse
from django.http import HttpResponseRedirect
from register.models import Company, UserProfile
from projects.models import Project, Task

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def dashboard(request):
    users = User.objects.all()
    active_users = User.objects.all().filter(is_active=True)
    companies = Company.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all()
    context = {
        'users': users,
        'active_users': active_users,
        'companies': companies,
        'projects': projects,
        'tasks': tasks,
    }
    return render(request, 'core/dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect(reverse('projects:task_list'))
    return render(request, 'core/index.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:index'))

def context(request):
    users = User.objects.all()
    active_users = User.objects.all().filter(is_active=True)
    companies = Company.objects.all()
    projects = Project.objects.all()
    tasks = Task.objects.all()
    context = {
        'users': users,
        'active_users': active_users,
        'companies': companies,
        'projects': projects,
        'tasks': tasks,
    }
    return context

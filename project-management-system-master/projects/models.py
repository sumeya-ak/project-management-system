from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


status = (
    ('1', 'Stuck'),
    ('2', 'Working'),
    ('3', 'Done'),
)

due = (
    ('1', 'On Due'),
    ('2', 'Overdue'),
    ('3', 'Done'),
)

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField('shortcut', blank=True)
    assign = models.ManyToManyField(User, related_name='assigned_projects')
    efforts = models.DurationField()
    status = models.CharField(max_length=7, choices=status, default='1')
    dead_line = models.DateField()
    company = models.ForeignKey('register.Company', on_delete=models.CASCADE, related_name='company_projects')
    complete_per = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(blank=True)
    add_date = models.DateField(auto_now_add=True)
    upd_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'projects_project'
        ordering = ['name']

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_tasks')
    assign = models.ManyToManyField(User, related_name='assigned_tasks')
    task_name = models.CharField(max_length=80)
    status = models.CharField(max_length=7, choices=status, default='1')
    due = models.CharField(max_length=7, choices=due, default='1')

    class Meta:
        db_table = 'projects_task'
        ordering = ['project', 'task_name']

    def __str__(self):
        return self.task_name
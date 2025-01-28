from django import forms
from django.utils.text import slugify
from .models import Task, Project
from register.models import Company
from django.contrib.auth.models import User

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

class TaskRegistrationForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    assign = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    task_name = forms.CharField(max_length=80)
    status = forms.ChoiceField(choices=status)
    due = forms.ChoiceField(choices=due)

    class Meta:
        model = Task
        fields = '__all__'

    def save(self, commit=True):
        task = super(TaskRegistrationForm, self).save(commit=False)
        task.project = self.cleaned_data['project']
        task.task_name = self.cleaned_data['task_name']
        task.status = self.cleaned_data['status']
        task.due = self.cleaned_data['due']
        
        if commit:
            task.save()
            assigns = self.cleaned_data['assign']
            task.assign.set(assigns)

        return task

    def __init__(self, *args, **kwargs):
        super(TaskRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ProjectRegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=80)
    assign = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    efforts = forms.DurationField()
    status = forms.ChoiceField(choices=status)
    dead_line = forms.DateField()
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    complete_per = forms.FloatField(min_value=0, max_value=100)
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Project
        fields = ['name', 'assign', 'efforts', 'status', 'dead_line', 'company', 'complete_per', 'description']

    def save(self, commit=True):
        project = super(ProjectRegistrationForm, self).save(commit=False)
        project.name = self.cleaned_data['name']
        project.slug = slugify(self.cleaned_data['name'])
        project.efforts = self.cleaned_data['efforts']
        project.status = self.cleaned_data['status']
        project.dead_line = self.cleaned_data['dead_line']
        project.company = self.cleaned_data['company']
        project.complete_per = self.cleaned_data['complete_per']
        project.description = self.cleaned_data['description']
        
        if commit:
            project.save()
            assigns = self.cleaned_data['assign']
            project.assign.set(assigns)

        return project

    def __init__(self, *args, **kwargs):
        super(ProjectRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Project Name'})
        self.fields['efforts'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Efforts'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['dead_line'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Dead Line'})
        self.fields['company'].widget.attrs.update({'class': 'form-control'})
        self.fields['complete_per'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Complete %'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Project description...'})
        self.fields['assign'].widget.attrs.update({'class': 'form-control'})
from django import forms
from .models import Task, Project, Todo










class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", 'priority', 'difficulty', 'approval_required',  'team', 'loops']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name_input_task', 'placeholder': 'Task Name'}),
            'team': forms.Select(attrs={'id': 'team_input_task', 'placeholder': 'Team'}),
            'priority': forms.Select(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                attrs={'id': 'priority_input_task'}
                ),
            'difficulty': forms.Select(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                attrs={'id': 'difficulty_input_task'}
            ),
            'approval_required': forms.Select(
                choices=[(True, 'Yes'), (False, 'No')],
                attrs={'id': 'difficulty_input_task'}
            ),
            'loops': forms.Select(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                attrs={'id': 'loops_input_task'}
                )
        }

class TaskTeamUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["team"]
        widgets = {
            'team': forms.Select(attrs={'id': 'team_input_task', 'placeholder': 'Team'}),
        }

class TaskLoopUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["loops"]
        widgets = {
            'loops': forms.Select(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                attrs={'id': 'loops_input_task'}
            )
        }

class TaskNameUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name"]
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name_input_task', 'placeholder': 'Task Name'}),
        }

class TaskPriorityUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["priority"]
        widgets = {
            'priority': forms.Select(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                attrs={'id': 'priority_input_task'}
            )
        }

class TaskDifficultyUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["difficulty"]
        widgets = {
            'difficulty': forms.Select(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                attrs={'id': 'difficulty_input_task'}
            )
        }

class TaskApprovalRequiredUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["approval_required"]
        widgets = {
            'approval_required': forms.Select(
                choices=[(True, 'Yes'), (False, 'No')],
                attrs={'id': 'difficulty_input_task'}
            )
        }










class ProjectTimeframeForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["start_date", "end_date"]
        widgets = {
            'start_date': forms.DateInput(attrs={'id': 'start_date_input_project', 'placeholder': 'Start Date', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'id': 'end_date_input_project', 'placeholder': 'End Date', 'type': 'date'})
        }







class TodoCreateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['description', 'done']
        widgets = {
            'description': forms.TextInput(attrs={
                'placeholder': 'What needs to be done?',
                'class': 'form-control',
            }),
            'done': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class TodoDoneForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["done"]
        widgets = {
            'done': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'onchange': 'this.form.submit()'  # ✅ Submit form on checkbox toggle
            })
        }
















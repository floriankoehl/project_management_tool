from django import forms
from .models import Team, Task, Project

class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "color"]
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name_input_team', 'placeholder': 'Task Name'}),
            'color': forms.TextInput(attrs={'type': 'color', 'id': 'color_input_team', 'placeholder': 'Task Color'})
            }

class TeamUpdateNameForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name"]
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name_input_team', 'placeholder': 'Task Name'}),
        }

class TeamUpdateColorForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["color"]
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color', 'id': 'color_input_team', 'placeholder': 'Task Color'})
        }









class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", 'team', 'loops']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name_input_task', 'placeholder': 'Task Name'}),
            'team': forms.Select(attrs={'id': 'team_input_task', 'placeholder': 'Team'}),
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


class ProjectTimeframeForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["start_date", "end_date"]
        widgets = {
            'start_date': forms.DateInput(attrs={'id': 'start_date_input_project', 'placeholder': 'Start Date', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'id': 'end_date_input_project', 'placeholder': 'End Date', 'type': 'date'})
        }




from django import forms
from .models import Team

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

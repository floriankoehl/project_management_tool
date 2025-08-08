from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Team, CustomUser, TeamMembership

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role']



# class CreateTeamMembershipForm(forms.ModelForm):
#     class Meta:
#         model = TeamMembership
#         fields = ''

























from django import forms
from users.models import Team, TeamMembership

class JoinTeamForm(forms.Form):
    team = forms.ModelChoiceField(
        queryset=Team.objects.none(),  # placeholder, overridden in __init__
        label="Select a team to join",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        # print(user)

        super().__init__(*args, **kwargs)

        joined_team_ids = TeamMembership.objects.filter(user=user).values_list("team_id", flat=True)
        available_teams = Team.objects.exclude(id__in=joined_team_ids)

        # print("🧠 [DEBUG] Available teams for user:", user)
        # for t in available_teams:
        #     print(f" - {t.name} (id={t.id})")

        self.fields["team"].queryset = available_teams





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








from django import forms
from users.models import TaskAssignment

class AssignUserToTaskForm(forms.ModelForm):
    class Meta:
        model = TaskAssignment
        fields = []  # no form fields

    def __init__(self, *args, **kwargs):
        self.task = kwargs.pop("task")
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if TaskAssignment.objects.filter(task=self.task, user=self.user).exists():
            return None

        assignment = TaskAssignment(task=self.task, user=self.user)  # ✅ manually set fields
        if commit:
            assignment.save()
        return assignment



# from django import forms
# from .models import TaskAssignment, CustomUser

class UserSelectForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        label="Select a user",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = TaskAssignment
        fields = ['user']





















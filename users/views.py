from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from distributor.models import Task
from .models import Team, TeamMembership, CustomUser, TaskAssignment
from .forms import TeamCreationForm, TeamUpdateNameForm, TeamUpdateColorForm, CustomUserCreationForm, JoinTeamForm, \
    AssignUserToTaskForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm







def profile_page(request, user_id):
    profile_user = get_object_or_404(CustomUser, id=user_id)
    task_assignment_team_member_mismatch_bool = False

    def has_mismatched_task_assignments(user):
        memberships = TeamMembership.objects.filter(user=user).values_list("team_id", flat=True)
        assignments = TaskAssignment.objects.filter(user=user).select_related("task")

        for assignment in assignments:
            if assignment.task.team_id not in memberships:
                return True  # 🚨 Mismatch found

        return False  # ✅ All assignments match teams

    if not has_mismatched_task_assignments(profile_user):
        task_assignment_team_member_mismatch_bool = True


    if request.method == "POST":
        join_team_form = JoinTeamForm(request.POST, user=profile_user)
        print("✅ [VIEW DEBUG] POST form instance:", join_team_form)
        print("✅ [VIEW DEBUG] Form fields:", join_team_form.fields.keys())
        if join_team_form.is_valid():
            team = join_team_form.cleaned_data["team"]
            TeamMembership.objects.get_or_create(user=profile_user, team=team)
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        join_team_form = JoinTeamForm(user=profile_user)
        print("✅ [VIEW DEBUG] GET form instance:", join_team_form)
        print("✅ [VIEW DEBUG] Form fields:", join_team_form.fields.keys())


    user_tasks = TaskAssignment.objects.filter(user=profile_user)

    context = {
        'join_team_form': join_team_form,
        'user': profile_user,
        'user_tasks': user_tasks,
        "task_assignment_team_member_mismatch_bool": task_assignment_team_member_mismatch_bool,
    }

    return render(request, "users/profile_page.html", context)




def assign_user_to_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    user = request.user

    if request.method == "POST":
        form = AssignUserToTaskForm(user=user, task=task)
        form.save()

        if not TeamMembership.objects.filter(user=user, team=task.team).exists():
            TeamMembership.objects.create(user=user, team=task.team)

        # return redirect('profile_page', user_id=user.id)

    return redirect(request.META.get("HTTP_REFERER", "/"))


def delete_task_assignment(request, task_assignment_id):
    task_asignment = get_object_or_404(TaskAssignment, id=task_assignment_id)
    task_asignment.delete()

    return redirect(request.META.get("HTTP_REFERER", "/"))
















def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, "users/register.html", context)


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }

    return render(request, "users/register.html", context)




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    context = {
        "form": form,
    }
    return render(request, 'users/login_view.html', context)





def logout_view(request):
    logout(request)
    return redirect('home')















def users(request):
    all_users = CustomUser.objects.all()
    return render(request, 'users/view_all_users_page.html', {"users": all_users})






# Create your views here.
def teams(request):
    all_teams = Team.objects.all()


    team_form = TeamCreationForm()
    context = {
        'team_form': team_form,
        'all_teams': all_teams
    }
    return render(request, 'users/teams.html', context)




def create_team(request):
    if request.method == "POST":
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teams')

        return render(request, 'users/teams.html', {'form': form})


def delete_team(request, id):
    if request.method == "POST":
        team = get_object_or_404(Team, pk=id)
        team.delete()
        return redirect('teams')



def edit_team_page(request, id):
    team = get_object_or_404(Team, pk=id)
    team_update_name_form = TeamUpdateNameForm(instance=team)
    team_update_color_form = TeamUpdateColorForm(instance=team)
    context = {
        'team': team,
        'team_update_name_form': team_update_name_form,
        'team_update_color_form': team_update_color_form
    }
    return render(request, 'users/edit_team_page.html', context)


def team_update_name(request, id):
    team = get_object_or_404(Team, pk=id)
    if request.method == "POST":
        form = TeamUpdateNameForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('edit_team_page', id)
    else:
        form = TeamUpdateNameForm(instance=team)

    return render(request, 'users/edit_team_page.html', {'form': form, 'team': team})



def team_update_color(request, id):
    team = get_object_or_404(Team, pk=id)
    if request.method == "POST":
        form = TeamUpdateColorForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('edit_team_page', id)
    else:
        form = TeamUpdateColorForm(instance=team)

    return render(request, 'users/edit_team_page.html', {'form': form, 'team': team})


























@login_required
def join_team_by_button(request, id):
    team = get_object_or_404(Team, pk=id)
    if request.method == "POST":
        if request.user.is_authenticated:

            TeamMembership.objects.get_or_create(team=team, user=request.user)

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)

    return redirect



def remove_user_from_team(request, team_id, user_id):
    team = get_object_or_404(Team, pk=team_id)
    user = get_object_or_404(CustomUser, pk=user_id)  # <- use your model here

    membership = TeamMembership.objects.filter(team=team, user=user).first()

    if request.method == "POST":
        membership.delete()

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)














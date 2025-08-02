from django.shortcuts import render, redirect
from .models import Team
from .forms import TeamCreationForm, TeamUpdateNameForm, TeamUpdateColorForm
from django.shortcuts import get_object_or_404

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
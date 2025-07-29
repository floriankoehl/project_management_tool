from django.shortcuts import render, redirect
from .forms import TeamCreationForm, TaskCreationForm, ProjectTimeframeForm

from .models import Team, Task, Project


# Create your views here.
def home(request):
    return render(request, 'distributor/home.html')




def teams(request):
    all_teams = Team.objects.all()


    team_form = TeamCreationForm()
    context = {
        'team_form': team_form,
        'all_teams': all_teams
    }
    return render(request, 'distributor/teams.html', context)

def create_team(request):
    if request.method == "POST":
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teams')
        else:
            form = TeamCreationForm()

        return render(request, 'distributor/teams.html', {'form': form})



def tasks(request):
    all_tasks = Task.objects.all()
    task_form = TaskCreationForm()
    context = {
        'all_tasks': all_tasks,
        'task_form': task_form
    }

    return render(request, 'distributor/tasks.html', context)




def create_task(request):
    if request.method == "POST":
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks')
        else:
            form = TaskCreationForm()
            return render(request, 'distributor/tasks.html', {'form': form})



def define_project_timeframe(request):
    existing_project_timeframe = Project.objects.first()

    if request.method == "POST":
        if existing_project_timeframe:
            form = ProjectTimeframeForm(request.POST, instance=existing_project_timeframe)

        else:
            form = ProjectTimeframeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = ProjectTimeframeForm(instance=existing_project_timeframe)

    return render(request, "home", {'form': form})


def change_project_page(request):
    return render(request, "distributor/change_project_timeframe.html")








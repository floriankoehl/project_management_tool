from django.shortcuts import render, redirect
from .forms import TeamCreationForm, TaskCreationForm, ProjectTimeframeForm

from .models import Team, Task, Project
from .utils import get_valid_possible_dependencies


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
        'task_form': task_form,
        "show_create_button": True
    }

    return render(request, 'distributor/tasks.html', context)


def create_task_page(request):
    all_tasks = Task.objects.all()
    task_form = TaskCreationForm()
    context = {
        'all_tasks': all_tasks,
        'task_form': task_form
    }
    return render(request, 'distributor/create_task_page.html', context)

def create_task(request):
    if request.method == "POST":
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            new_task = form.save()
            return redirect('add_dependency_page', new_task.id)
        else:
            form = TaskCreationForm()
            return render(request, 'distributor/tasks.html', {'form': form})


def display_task(request, id):
    task = Task.objects.get(pk=id)
    return render(request, 'distributor/display_task.html', {'task': task})

def edit_task(request, id):
    task = Task.objects.get(pk=id)
    return render(request, 'distributor/edit_task.html', {'task': task})



def add_dependency_page(request, id):
    task_to_be_modified = Task.objects.get(id=id)

    context = {
        'possible_deps': get_valid_possible_dependencies(task_to_be_modified),
        'task': task_to_be_modified,
    }
    return render(request, 'distributor/add_dep_task.html', context)


def add_dependency(request, id):
    if request.method == "POST":
        dep_to_be_added = request.POST.get('dep_to_be_added')
        task_to_be_modified = Task.objects.get(id=id)
        task_to_be_modified.initial_dependencies.add(dep_to_be_added)
        task_to_be_modified.save()

        referer = request.META.get('HTTP_REFERER')  # where the request came from
        return redirect(referer or 'tasks')  # fallback if header is missing


def delete_dependency(request, id):
    if request.method == "POST":
        task_to_be_modified = Task.objects.get(id=id)
        dep_to_be_removed = request.POST.get('dep_to_be_removed')
        task_to_be_modified.initial_dependencies.remove(dep_to_be_removed)
        task_to_be_modified.save()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer or 'tasks')



def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(pk=id)
        task.delete()
        return redirect('tasks')







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

    return render(request, "distributor/home", {'form': form})


def change_project_page(request):
    return render(request, "distributor/change_project_timeframe.html")








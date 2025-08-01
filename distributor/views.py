from django.shortcuts import render, redirect, get_object_or_404
from .forms import TeamCreationForm, TaskCreationForm, ProjectTimeframeForm, TaskTeamUpdateForm, TaskLoopUpdateForm, \
    TaskNameUpdateForm, TeamUpdateNameForm, TeamUpdateColorForm, TaskPriorityUpdateForm, TaskDifficultyUpdateForm, \
    TaskApprovalRequiredUpdateForm, TodoCreateForm, TodoDoneForm

from .models import Team, Task, Project, TaskLoop, Todo
from .timeline import plan_order_of_task_loops
from .utils import get_valid_possible_dependencies, create_task_loop_objects


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

def delete_team(request, id):
    if request.method == "POST":
        team = Team.objects.get(pk=id)
        team.delete()
        return redirect('teams')



def edit_team_page(request, id):
    team = Team.objects.get(pk=id)
    team_update_name_form = TeamUpdateNameForm(instance=team)
    team_update_color_form = TeamUpdateColorForm(instance=team)
    context = {
        'team': team,
        'team_update_name_form': team_update_name_form,
        'team_update_color_form': team_update_color_form
    }
    return render(request, 'distributor/edit_team_page.html', context)


def team_update_name(request, id):
    team = Team.objects.get(pk=id)
    if request.method == "POST":
        form = TeamUpdateNameForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('edit_team_page', id)
    else:
        form = TeamUpdateNameForm(instance=team)

    return render(request, 'edit_team_page', {'form': form, 'team': team})


def team_update_color(request, id):
    team = Team.objects.get(pk=id)
    if request.method == "POST":
        form = TeamUpdateColorForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('edit_team_page', id)
    else:
        form = TeamUpdateColorForm(instance=team)

    return render(request, 'edit_team_page', {'form': form, 'team': team})


def tasks(request):
    all_tasks = Task.objects.all().order_by('team')
    task_form = TaskCreationForm()
    create_task_loop_objects()
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

            return redirect('edit_task_page', new_task.id)
        else:
            form = TaskCreationForm()
            return render(request, 'distributor/tasks.html', {'form': form})


def display_task(request, id):
    task = Task.objects.get(pk=id)
    return render(request, 'distributor/display_task.html', {'task': task})



def edit_task_page(request, id):
    task = Task.objects.get(pk=id)
    task_name_update_form = TaskNameUpdateForm(instance=task)
    task_team_update_form = TaskTeamUpdateForm(instance=task)
    task_loop_update_form = TaskLoopUpdateForm(instance=task)
    task_priorty_update_form = TaskPriorityUpdateForm(instance=task)
    task_difficulty_update_form = TaskDifficultyUpdateForm(instance=task)
    task_approval_required_update_form = TaskApprovalRequiredUpdateForm(instance=task)
    todo_form = TodoCreateForm()
    todo_done_form = TodoDoneForm()

    context = {
        'task': task,
        'task_name_update_form': task_name_update_form,
        'task_team_update_form': task_team_update_form,
        'task_loop_update_form': task_loop_update_form,
        'task_priorty_update_form': task_priorty_update_form,
        'task_difficulty_update_form': task_difficulty_update_form,
        'task_approval_required_update_form': task_approval_required_update_form,
        'todo_form': todo_form,
        'todo_done_form': todo_done_form,
    }
    return render(request, 'distributor/edit_task_page.html', context)



def task_priority_update(request, id):
    task = Task.objects.get(pk=id)

    if request.method == "POST":
        form = TaskPriorityUpdateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('edit_task_page', task.id)

    else:
        form = TaskPriorityUpdateForm(instance=task)

    return render(request, 'edit_task_pages.html', {'TaskTeamUpdateForm': form, 'task': task})


def task_difficulty_update(request, id):
    task = Task.objects.get(pk=id)

    if request.method == "POST":
        form = TaskDifficultyUpdateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('edit_task_page', task.id)

    else:
        form = TaskDifficultyUpdateForm(instance=task)

    return render(request, 'edit_task_pages.html', {'TaskTeamUpdateForm': form, 'task': task})



def task_approval_required_update(request, id):
    task = Task.objects.get(pk=id)

    if request.method == "POST":
        form = TaskApprovalRequiredUpdateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('edit_task_page', task.id)

    else:
        form = TaskApprovalRequiredUpdateForm(instance=task)

    return render(request, 'edit_task_pages.html', {'TaskTeamUpdateForm': form, 'task': task})





def task_name_update(request, id):
    task = Task.objects.get(pk=id)

    if request.method == "POST":
        form = TaskNameUpdateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('edit_task_page', task.id)

    else:
        form = TaskNameUpdateForm(instance=task)

    return render(request, 'edit_task_pages.html', {'TaskTeamUpdateForm': form, 'task': task})

def task_team_update(request, id):
    task = Task.objects.get(pk=id)

    if request.method == "POST":
        form = TaskTeamUpdateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('edit_task_page', task.id)

    else:
        form = TaskTeamUpdateForm(instance=task)

    return render(request, 'edit_task_page.html', {'TaskTeamUpdateForm': form, 'task': task})

def task_loops_update(request, id):
    task = Task.objects.get(pk=id)

    if request.method == "POST":
        form = TaskLoopUpdateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('edit_task_page', task.id)

    else:
        form = TaskLoopUpdateForm(instance=task)

    return render(request, 'edit_task_page.html', {'TaskTeamUpdateForm': form, 'task': task})


# def edit_task_page(request, id):
#     task = Task.objects.get(pk=id)
#     return render(request, 'distributor/edit_task_page.html', {'task': task})

# def edit_task(request, id):
#     task = Task.objects.get(pk=id)
#
#     if request.method == "POST":
#         form = TaskCreationForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect("display_task", task.id)
#     else:
#         form = TaskCreationForm(instance=task)
#
#     return render(request, "distributor/edit_task_page.html", {
#         "task": task,
#         "form": form
#     })


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




def timeline(request):
    order_counter = plan_order_of_task_loops()   # this returns the max value assigned
    order_range = range(order_counter + 1)       # ✅ include all possible values

    all_task_loops = TaskLoop.objects.all().order_by('task__team')

    context = {
        'all_task_loops': all_task_loops,
        'order_range': order_range,
    }

    return render(request, 'distributor/timeline.html', context)


def add_todo(request, id):
    task = Task.objects.get(pk=id)
    if request.method == "POST":
        form = TodoCreateForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.task = task
            todo.save()

            # Redirect back to the previous page
            return redirect(request.META.get('HTTP_REFERER', '/'))  # fallback to '/' if no referrer
    else:
        form = TodoCreateForm()

    return render(request, 'your_template.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect
from .models import Todo
from .forms import TodoDoneForm

def todo_done_update(request, id):
    todo = get_object_or_404(Todo, pk=id)

    if request.method == "POST":
        form = TodoDoneForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(request.META.get('HTTP_REFERER', '/'))




from django.shortcuts import render, redirect, get_object_or_404
from .forms import *

from .models import Task, Project, TaskLoop, Todo
from .timeline import plan_order_of_task_loops, compare_max_order_number_to_timeframe
from .utils import get_valid_possible_dependencies, create_task_loop_objects, get_days_in_timeframe


# Create your views here.













def tasks(request):
    all_tasks = Task.objects.all().order_by('team')
    task_form = TaskCreationForm()
    context = {
        'all_tasks': all_tasks,
        'task_form': task_form,
        "show_create_button": True
    }

    return render(request, 'distributor/tasks.html', context)




def reload_tasks(request):
    create_task_loop_objects()

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('tasks')




def reload_all(request):
    create_task_loop_objects()
    num_days = len(get_days_in_timeframe())

    compare_max_order_number_to_timeframe(num_days)

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('home')






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

            source_page = request.POST.get("source", "")


            if source_page == "create_task_page":
                return redirect('edit_task_page', new_task.id)
            else:
                referer = request.META.get('HTTP_REFERER')
                return redirect(referer)

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

    return render(request, 'distributor/edit_task_page.html', {'TaskTeamUpdateForm': form, 'task': task})


def task_difficulty_update(request, id):
    task = Task.objects.get(pk=id)

    if request.method == "POST":
        form = TaskDifficultyUpdateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('edit_task_page', task.id)

    else:
        form = TaskDifficultyUpdateForm(instance=task)

    return render(request, 'distributor/edit_task_page.html', {'TaskTeamUpdateForm': form, 'task': task})



def task_approval_required_update(request, id):
    task = Task.objects.get(pk=id)

    if request.method == "POST":
        form = TaskApprovalRequiredUpdateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('edit_task_page', task.id)

    else:
        form = TaskApprovalRequiredUpdateForm(instance=task)

    return render(request, 'distributor/edit_task_page.html', {'TaskTeamUpdateForm': form, 'task': task})





def task_name_update(request, id):
    task = Task.objects.get(pk=id)

    if request.method == "POST":
        form = TaskNameUpdateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('edit_task_page', task.id)

    else:
        form = TaskNameUpdateForm(instance=task)

    return render(request, 'distributor/edit_task_page.html', {'TaskTeamUpdateForm': form, 'task': task})

def task_team_update(request, id):
    task = Task.objects.get(pk=id)

    if request.method == "POST":
        form = TaskTeamUpdateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('edit_task_page', task.id)

    else:
        form = TaskTeamUpdateForm(instance=task)

    return render(request, 'distributor/edit_task_page.html', {'TaskTeamUpdateForm': form, 'task': task})

def task_loops_update(request, id):
    task = Task.objects.get(pk=id)

    if request.method == "POST":
        form = TaskLoopUpdateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('edit_task_page', task.id)

    else:
        form = TaskLoopUpdateForm(instance=task)

    return render(request, 'distributor/edit_task_page.html', {'TaskTeamUpdateForm': form, 'task': task})


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




from django.views.decorators.http import require_POST

@require_POST
def add_dependency_training_page(request):
    from_id = request.POST.get("from_id")
    to_id = request.POST.get("to_id")
    source = request.POST.get("source", "")

    try:
        from_task = Task.objects.get(id=from_id)
        to_task = Task.objects.get(id=to_id)

        to_task.initial_dependencies.add(from_task)

        if source == "training_page":
            return redirect("training_page")
        else:
            return redirect("edit_task_page", to_task.id)

    except Task.DoesNotExist:
        return redirect("training_page")  # fallback in case of invalid ID

















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



from users.models import Team
def timeline(request):
    team_id = request.GET.get("team")
    project = Project.objects.first()
    order_counter = project.order_counter  # this returns the max value assigned
    day_list = get_days_in_timeframe()
    all_teams = Team.objects.all()
    rest_render_days_number_range = len(day_list) - order_counter -1
    all_tasks = Task.objects.all()

    # print(order_counter)

    order_range = range(order_counter + 1)       # ✅ include all possible values

    all_task_loops = TaskLoop.objects.all().order_by('task__team')

    # In your view
    # for taskloop in all_task_loops:
    #     taskloop.order_end = taskloop.order_number + taskloop.duration
    #     taskloop.save()

    if team_id:
        all_task_loops = TaskLoop.objects.filter(task__team_id=team_id)
    else:
        all_task_loops = TaskLoop.objects.all().order_by('task__team')

    context = {
        'all_tasks': all_tasks,
        'all_task_loops': all_task_loops,
        'all_teams': all_teams,
        'order_range': order_range,
        'day_list': day_list,
        "request": request,
        "rest_render_days_number_range": range(rest_render_days_number_range),
    }

    # parent_function(TaskLoop.objects.all().order_by('order_number'))
    # for loop in all_task_loops:
    #     print(loop, loop.order_number)

    return render(request, 'distributor/timeline.html', context)




def reload_timeline(request):
    num_days = len(get_days_in_timeframe())

    compare_max_order_number_to_timeframe(num_days)

    # from distributor.models import TaskLoop
    # for loop in TaskLoop.objects.all():
    #     print(loop, loop.order_number)

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect("timeline")





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






def training_page(request):
    tasks = Task.objects.prefetch_related('initial_dependencies')

    graph_nodes = []
    graph_edges = []

    for task in tasks:
        graph_nodes.append({"id": task.id, "label": task.name})
        for dep in task.initial_dependencies.all():
            graph_edges.append({"from": dep.id, "to": task.id})

    context = {
        "graph_nodes": graph_nodes,
        "graph_edges": graph_edges
    }

    return render(request, 'distributor/training_page.html', context)
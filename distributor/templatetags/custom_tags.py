

from django import template
from distributor.models import Team, Task, TaskLoop
from distributor.utils import get_valid_possible_dependencies
from ..forms import *

register = template.Library()

@register.inclusion_tag('components/all_teams.html')
def show_all_teams():
    teams = Team.objects.all()
    return {'teams': teams}


@register.inclusion_tag('components/all_tasks.html')
def show_all_tasks():
    tasks = Task.objects.all().order_by('team')
    return {'all_tasks': tasks}

@register.inclusion_tag('components/view_task.html')
def view_task(task_id):
    task = Task.objects.get(pk=task_id)
    return {'task': task}



@register.inclusion_tag('components/update_dependencies.html')
def update_dependencies(task_id):
    task = Task.objects.get(pk=task_id)
    possible_deps = get_valid_possible_dependencies(task)
    return {
        'task': task,
        'possible_deps': possible_deps
    }

@register.inclusion_tag('components/comp_display_single_team.html')
def comp_display_single_team(team_id):
    team = Team.objects.get(pk=team_id)
    return {'team': team}

@register.inclusion_tag('components/comp_all_taskloop_objects.html')
def all_task_loop_objects():
    all_task_loop_objects = TaskLoop.objects.all()
    return {'task_loop_objects': all_task_loop_objects}

from distributor.models import TaskLoop, TaskLoopDependency

@register.inclusion_tag('components/comp_display_task_loop_object.html')
def comp_display_task_loop_object(task_loop_id):
    task_loop_object = TaskLoop.objects.get(pk=task_loop_id)

    # Get all dependencies where this TaskLoop is the dependent
    all_deps = TaskLoopDependency.objects.filter(
        dependent_task_loop=task_loop_object
    ).select_related("master_task_loop")

    # Group by type
    dependencies_by_type = {
        "defined": [],
        "prior_loop": [],
        "cross_loop": [],
    }

    for dep in all_deps:
        dependencies_by_type[dep.type].append(dep.master_task_loop)

    # Get reverse dependencies too (for "Required by" list)
    required_by = TaskLoopDependency.objects.filter(
        master_task_loop=task_loop_object
    ).select_related("dependent_task_loop")

    return {
        "task_loop_object": task_loop_object,
        "initial_dependencies": task_loop_object.task.initial_dependencies.all(),
        "defined_deps": dependencies_by_type["defined"],
        "prior_loop_deps": dependencies_by_type["prior_loop"],
        "cross_loop_deps": dependencies_by_type["cross_loop"],
        "required_by": [dep.dependent_task_loop for dep in required_by],
    }


@register.inclusion_tag('components/edit_task_comp.html')
def edit_task_comp(task_id):
    task = Task.objects.get(pk=task_id)
    task_name_update_form = TaskNameUpdateForm(instance=task)
    task_team_update_form = TaskTeamUpdateForm(instance=task)
    task_loop_update_form = TaskLoopUpdateForm(instance=task)
    task_priorty_update_form = TaskPriorityUpdateForm(instance=task)
    task_difficulty_update_form = TaskDifficultyUpdateForm(instance=task)
    task_approval_required_update_form = TaskApprovalRequiredUpdateForm(instance=task)

    context = {
        'task': task,
        'task_name_update_form': task_name_update_form,
        'task_team_update_form': task_team_update_form,
        'task_loop_update_form': task_loop_update_form,
        'task_priorty_update_form': task_priorty_update_form,
        'task_difficulty_update_form': task_difficulty_update_form,
        'task_approval_required_update_form': task_approval_required_update_form
    }


    return context


@register.inclusion_tag('components/comp_show_all_task_loop_objects_of_one_task_loop.html')
def comp_show_all_task_loop_objects_of_one_task_loop(task_id):
    task = Task.objects.get(pk=task_id)
    task_loop_objects = task.taskloop_set.all()
    return {'task_loop_objects': task_loop_objects}



@register.filter
def dict_get(d, key):
    return d.get(key)


@register.filter
def heat_color(magnitude, params="240,100,50;120,100,50"):
    """
    Converts a magnitude (0–100) into an HSL color that transitions from a high color to a low color.

    Format:
        "hue_high,sat_high,light_high;hue_low,sat_low,light_low"

    Example:
        "0,100,50;60,100,90" → Red (high) to Yellow (low)
        "240,100,50;120,80,70" → Blue (high) to Green (low)
        "0,100,50;0,0,100" → Red to White

    Usage:
        {{ taskloop.magnitude|heat_color:"240,100,50;120,100,50" }}
    """
    try:
        mag = float(magnitude)
        mag = max(0, min(100, mag)) / 100  # normalize to 0.0 – 1.0

        # Split the parameters into high and low
        high_part, low_part = params.split(";")
        hue_high, sat_high, light_high = map(float, high_part.split(","))
        hue_low, sat_low, light_low = map(float, low_part.split(","))

        # Interpolate each component
        hue = hue_low + (hue_high - hue_low) * mag
        sat = sat_low + (sat_high - sat_low) * mag
        light = light_low + (light_high - light_low) * mag

        return f"hsl({hue:.0f}, {sat:.0f}%, {light:.0f}%)"
    except Exception as e:
        return "white"


from ..forms import TodoDoneForm, TodoCreateForm

@register.inclusion_tag('components/todo_component.html')
def todo_component(task):
    return {
        'task': task,
        'todo_form': TodoCreateForm,
        'todo_done_update': TodoDoneForm,
    }


@register.inclusion_tag('components/display_schedule_log.html')
def display_schedule_log(taskloop):
    schedule_log_messages = taskloop.activitylog_set.filter(type='schedule_log')

    return {'schedule_log_messages': schedule_log_messages}


@register.inclusion_tag('components/display_dep_log_task_loop.html')
def display_dep_log_task_loop(task_loop):
    dep_log_messages = task_loop.activitylog_set.filter(type='setup_up_dependencies_taskloop')
    return {'dep_log_messages': dep_log_messages}



@register.inclusion_tag('components/display_reload_buttons.html')
def display_reload_buttons():
    return {}

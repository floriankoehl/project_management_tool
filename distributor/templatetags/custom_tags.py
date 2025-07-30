

from django import template
from distributor.models import Team, Task
from distributor.utils import get_valid_possible_dependencies

register = template.Library()

@register.inclusion_tag('components/all_teams.html')
def show_all_teams():
    teams = Team.objects.all()
    return {'teams': teams}


@register.inclusion_tag('components/all_tasks.html')
def show_all_tasks():
    tasks = Task.objects.all()
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






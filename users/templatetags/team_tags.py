from django import template
from distributor.models import Task, TaskLoop
from distributor.utils import get_valid_possible_dependencies
from ..forms import *

register = template.Library()



@register.inclusion_tag('components/comp_display_single_team.html')
def comp_display_single_team(team_id):
    team = Team.objects.get(pk=team_id)
    return {'team': team}


@register.inclusion_tag('components/all_teams.html')
def show_all_teams():
    teams = Team.objects.all()
    return {'teams': teams}


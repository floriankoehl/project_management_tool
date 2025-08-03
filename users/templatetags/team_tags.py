from django import template
from django.contrib.auth import get_user_model  # ✅ correct
User = get_user_model()


from distributor.models import Task, TaskLoop
from distributor.utils import get_valid_possible_dependencies
from ..forms import *

register = template.Library()



@register.inclusion_tag('components/comp_display_single_team.html')
def comp_display_single_team(team_id):
    team = Team.objects.get(pk=team_id)
    memberships = TeamMembership.objects.filter(team=team)

    for membership in memberships:
        print(membership.user)

    return {'team': team, 'memberships': memberships}

@register.inclusion_tag('components/comp_display_single_team_medium.html')
def comp_display_single_team_medium(team_id):
    team = Team.objects.get(pk=team_id)
    memberships = TeamMembership.objects.filter(team=team)

    for membership in memberships:
        print(membership.user)

    return {'team': team, 'memberships': memberships}


@register.inclusion_tag('components/all_teams.html')
def show_all_teams():
    teams = Team.objects.all()
    return {'teams': teams}


@register.inclusion_tag("components/display_single_user.html")
def display_single_user(user_id):
    user = User.objects.get(pk=user_id)
    return {'user': user}



@register.inclusion_tag("components/display_all_users.html")
def display_all_users():
    users = User.objects.all()
    return {'users': users}





















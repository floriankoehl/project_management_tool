from django import template
from django.contrib.auth import get_user_model  # ✅ correct
User = get_user_model()


from distributor.models import Task, TaskLoop
from distributor.utils import get_valid_possible_dependencies
from ..forms import *

register = template.Library()



@register.inclusion_tag('components/comp_display_single_team.html', takes_context=True)
def comp_display_single_team(context, team):
    user = context.get("user", None)
    memberships = TeamMembership.objects.filter(team=team)

    # for membership in memberships:
    #     print(membership.user)

    return {'team': team, 'memberships': memberships, 'user': user}

@register.inclusion_tag('components/comp_display_single_team_medium.html', takes_context=True)
def comp_display_single_team_medium(context, team_id):
    user = context.get("user", None)
    team = Team.objects.get(pk=team_id)
    memberships = TeamMembership.objects.filter(team=team)

    # for membership in memberships:
    #     print(membership.user)

    return {'team': team, 'memberships': memberships, 'user': user}


@register.inclusion_tag('components/all_teams.html', takes_context=True)
def show_all_teams(context):
    user = context.get("user", None)
    teams = Team.objects.all()
    return {'teams': teams, 'user': user}



@register.inclusion_tag("components/display_single_user.html")
def display_single_user(profile_user):
    team_memberships = TeamMembership.objects.filter(user=profile_user)
    task_assignments = TaskAssignment.objects.filter(user=profile_user)
    return {'profile_user': profile_user, "team_memberships": team_memberships, 'task_assignments': task_assignments}



@register.inclusion_tag("components/display_all_users.html")
def display_all_users():
    users = User.objects.all()
    return {'users': users}












@register.inclusion_tag("components/user_page_team_overview.html")
def user_page_team_overview(profile_user):
    memberships = TeamMembership.objects.filter(user=profile_user)
    join_team_form = JoinTeamForm(user=profile_user)
    context = {
        'memberships': memberships,
        'profile_user': profile_user,
        'join_team_form': join_team_form
    }

    return context



@register.inclusion_tag("components/user_page_task_overview.html")
def user_page_task_overview(profile_user):
    task_assignments = TaskAssignment.objects.filter(user=profile_user).order_by('task__team')
    context = {
        'task_assignments': task_assignments,
    }

    return context





































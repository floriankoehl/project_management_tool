from django.forms import ModelForm

from users.models import Message
from .forms import ProjectTimeframeForm, DefineCurrentDate
from .models import Project

def global_project_timeframe_form(request):
    return {
        "global_project_timeframe_form": ProjectTimeframeForm(),
    }

def global_project_timeframe(request):
    project_time_frame = Project.objects.first()
    if project_time_frame:
        return {
            "global_project_timeframe": project_time_frame,
        }
    else:
        return {
            "global_project_timeframe": 'No values picked yet',
        }


def global_define_current_date_form(request):
    return {
        "global_define_current_date_form": DefineCurrentDate(),
    }


def global_project_info(request):
    project = Project.objects.first()
    if project:
        return {
            "project": project,
        }
    else:
        return {
            "project": 'No values picked yet',
        }


from users.models import Message

def global_number_new_messages_user(request):
    if request.user.is_authenticated:
        number_new_messages = Message.objects.filter(
            user=request.user, status="unread"
        ).count()
    else:
        number_new_messages = 0

    return {
        "number_new_messages": number_new_messages
    }

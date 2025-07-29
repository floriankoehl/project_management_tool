from .forms import ProjectTimeframeForm
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


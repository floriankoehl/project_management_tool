from django.contrib import admin
from .models import Team, Task, TaskLoop, Project


# Register your models here.
admin.site.register(Team)
admin.site.register(Task)
admin.site.register(TaskLoop)
admin.site.register(Project)
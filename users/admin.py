from django.contrib import admin
from .models import CustomUser, Team, TeamMembership

from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Team)
admin.site.register(TeamMembership)


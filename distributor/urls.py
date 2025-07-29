from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams', views.teams, name='teams'),
    path('tasks', views.tasks, name='tasks'),
    path('create_team', views.create_team, name='create_team'),
    path('create_task', views.create_task, name='create_task'),
    path('define_project_timeframe', views.define_project_timeframe, name='define_project_timeframe'),
    path("change_project_page", views.change_project_page, name='change_project_page'),
]
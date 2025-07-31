from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams', views.teams, name='teams'),
    path('tasks', views.tasks, name='tasks'),
    path('create_team', views.create_team, name='create_team'),
    path('create_task_page', views.create_task_page, name='create_task_page'),
    path('create_task', views.create_task, name='create_task'),
    path('define_project_timeframe', views.define_project_timeframe, name='define_project_timeframe'),
    path("change_project_page", views.change_project_page, name='change_project_page'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
    path('add_dependency/<int:id>/', views.add_dependency, name='add_dependency'),
    path('add_dependency_page/<int:id>/', views.add_dependency_page, name='add_dependency_page'),
    path('delete_dependency/<int:id>/', views.delete_dependency, name='delete_dependency'),
    path('display_task/<int:id>/', views.display_task, name='display_task'),
    path('edit_task_page/<int:id>/', views.edit_task_page, name='edit_task_page'),
    path('delete_team/<int:id>/', views.delete_team, name='delete_team'),
    path('task_team_update/<int:id>/', views.task_team_update, name='task_team_update'),
    path('task_loops_update/<int:id>/', views.task_loops_update, name='task_loops_update'),
    path('task_name_update/<int:id>/', views.task_name_update, name='task_name_update'),
    path('edit_team_page/<int:id>/', views.edit_team_page, name='edit_team_page'),
    path('team_update_name/<int:id>/', views.team_update_name, name='team_update_name'),
    path('team_update_color/<int:id>/', views.team_update_color, name='team_update_color'),
    path('task_priority_update/<int:id>/', views.task_priority_update, name='task_priority_update'),
    path('task_approval_required_update/<int:id>/', views.task_approval_required_update, name='task_approval_required_update'),
    path('task_difficulty_update/<int:id>/', views.task_difficulty_update, name='task_difficulty_update'),
    path('timeline', views.timeline, name='timeline'),
    # path('edit_task/<int:id>/', views.edit_task, name='edit_task'),

]